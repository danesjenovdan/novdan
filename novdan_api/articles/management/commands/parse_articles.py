import time
from typing import Optional

import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_datetime
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.core.validators import URLValidator
from django.utils import timezone
from django.utils.html import strip_tags
from meta_tags_parser.parse import parse_meta_tags_from_source
from meta_tags_parser.structs import WhatToParse
from rss_parser import AtomParser, RSSParser
from rss_parser.models import XMLBaseModel
from rss_parser.models.atom import Atom
from rss_parser.models.atom.entry import Entry
from rss_parser.models.atom.feed import Feed
from rss_parser.models.rss import RSS
from rss_parser.models.rss.channel import Channel
from rss_parser.models.rss.item import Item
from rss_parser.models.types.date import DateTimeOrStr
from rss_parser.models.types.only_list import OnlyList
from rss_parser.models.types.tag import Tag
from rss_parser.pydantic_proxy import import_v1_pydantic
from sentry_sdk import capture_exception, capture_message, push_scope

from ...models import Article, Medium

pydantic = import_v1_pydantic()


# Fix non standard rss feeds
class CustomItem(Item, XMLBaseModel):
    category: Optional[OnlyList[Tag[str]]] = None
    enclosure: Optional[OnlyList[Tag[str]]] = None


class CustomChannel(Channel, XMLBaseModel):
    items: Optional[OnlyList[Tag[CustomItem]]] = pydantic.Field(
        alias="item", default=[]
    )


class CustomSchema(RSS, XMLBaseModel):
    channel: Tag[CustomChannel]


# Fix for non standard atom feeds
class MediaGroup(XMLBaseModel):
    description: Optional[Tag[str]] = pydantic.Field(
        alias="media:description", default=None
    )
    thumbnails: Optional[OnlyList[Tag[XMLBaseModel]]] = pydantic.Field(
        alias="media:thumbnail", default=[]
    )


class CustomEntry(Entry, XMLBaseModel):
    media_groups: Optional[OnlyList[Tag[MediaGroup]]] = pydantic.Field(
        alias="media:group", default=[]
    )


class CustomFeed(Feed, XMLBaseModel):
    updated: Optional[Tag[DateTimeOrStr]]
    entries: Optional[OnlyList[Tag[CustomEntry]]] = pydantic.Field(
        alias="entry", default=[]
    )


class CustomAtomSchema(Atom, XMLBaseModel):
    feed: Tag[CustomFeed]


class DontRetryException(Exception):
    pass


def requests_get_with_retries(url, retries=5, delay=15, **kwargs):
    for attempt in range(retries):
        try:
            response = requests.get(url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if "www.youtube.com/feeds/videos.xml" in url:
                # do not retry youtube feed requests it just fails sometimes
                raise DontRetryException
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise e


class Command(BaseCommand):
    help = "Parse articles from Media RSS feeds"

    def is_url(self, url):
        val = URLValidator()
        try:
            val(url)
        except ValidationError:
            return False
        return True

    def update_article_image_url(self, article, image_url):
        if article.image_url:
            return

        def update_image_url(image_url):
            article.image_url = image_url[:512]
            article.save()
            self.stdout.write(f"     > updated image_url: {article.id}")

        if image_url and self.is_url(image_url):
            update_image_url(image_url)
            return

        time.sleep(3)  # wait to avoid rate limiting
        try:
            response = requests_get_with_retries(article.url, timeout=30)
        except DontRetryException:
            self.stdout.write(f"     > error updating image_url: DontRetryException")
            return
        except requests.exceptions.RequestException as e:
            self.stdout.write(f"     > error updating image_url: {e}")
            return

        def find_og_image(tags_group):
            for one_tag in tags_group.open_graph:
                if one_tag.name == "image" and one_tag.value:
                    return one_tag.value
            for one_tag in tags_group.twitter:
                if one_tag.name == "image" and one_tag.value:
                    return one_tag.value
            return None

        tags_group = parse_meta_tags_from_source(
            response.text,
            what_to_parse=(WhatToParse.OPEN_GRAPH, WhatToParse.TWITTER),
        )
        image_url = find_og_image(tags_group)

        if image_url and self.is_url(image_url):
            update_image_url(image_url)
            return

        image_css_selector = article.medium.image_css_selector or "article img"

        soup = BeautifulSoup(response.text, "html.parser")
        image = soup.select_one(image_css_selector)
        image_url = image.get("src") if image else None
        if image_url and self.is_url(image_url):
            update_image_url(image_url)
            return

    def is_atom_feed(self, data: str) -> bool:
        return "<feed" in data[:1000] and "http://www.w3.org/2005/Atom" in data[:1000]

    def parse_rss_feed(self, medium, url):
        now = timezone.now()

        self.stdout.write(f" > feed url: {url}")

        try:
            time.sleep(3)  # wait to avoid rate limiting
            response = requests_get_with_retries(url, timeout=30)

            response_text = response.text
            # fix random problems with feeds
            response_text = response_text.replace("<title>&nbsp;", "<title>")

            feed_type = "Atom" if self.is_atom_feed(response_text) else "RSS"
            self.stdout.write(f"   > feed type: {feed_type}")

            if feed_type == "Atom":
                rss = AtomParser.parse(response_text, schema=CustomAtomSchema)
                self.stdout.write(f"   > title: {rss.feed.title.content}")
                self.stdout.write(f"   > found items: {len(rss.feed.entries)}")
            else:
                rss = RSSParser.parse(response_text, schema=CustomSchema)
                self.stdout.write(f"   > title: {rss.channel.title.content}")
                self.stdout.write(f"   > found items: {len(rss.channel.items)}")
            self.stdout.write("")

            items = rss.feed.entries if feed_type == "Atom" else rss.channel.items
            for item in items:
                title = item.title.content
                if len(title) > 256:
                    title = title[:253] + "..."

                self.stdout.write(f"   > {title[:67]}")

                link = item.links[0] if hasattr(item, "links") and item.links else None
                if feed_type == "Atom":
                    link_content = link.attributes.get("href", None) if link else None
                elif feed_type == "RSS":
                    link_content = link.content if link else None

                if link_content and not link_content.startswith("http"):
                    if link_content.startswith("//"):
                        link_content = f"http:{link_content}"
                    if "://" not in link_content:
                        link_content = f"http://{link_content}"

                if not self.is_url(link_content):
                    with push_scope() as scope:
                        scope.set_extra("command", "parse_articles")
                        scope.set_extra("rss_url", url)
                        capture_message(f"Invalid url: {link_content}")
                    self.stdout.write(f"     > invalid url: {link_content}")
                    self.stdout.write("")
                    print(link)
                    continue

                url = link_content[:512]
                description = ""
                if feed_type == "RSS":
                    if item.description and item.description.content:
                        description = strip_tags(item.description.content)
                elif feed_type == "Atom":
                    if item.summary and item.summary.content:
                        description = strip_tags(item.summary.content)
                    elif item.content and item.content.content:
                        description = strip_tags(item.content.content)
                    elif item.media_groups:
                        for mg in item.media_groups:
                            if mg.description and mg.description.content:
                                description = strip_tags(mg.description.content)
                                break
                if len(description) > 256:
                    description = description[:253] + "..."

                if feed_type == "RSS":
                    guid = item.guid.content if item.guid else None
                elif feed_type == "Atom":
                    guid = item.id.content if item.id else None

                if not guid:
                    guid = link_content
                if not guid:
                    guid = item.title.content
                if guid and len(guid) > 256:
                    guid = guid[:253] + "..."

                if feed_type == "RSS":
                    pub_date = item.pub_date.content if item.pub_date else None
                elif feed_type == "Atom":
                    pub_date = item.published.content if item.published else None

                if pub_date and isinstance(pub_date, str):
                    pub_date = parse_datetime(pub_date)
                if not pub_date:
                    pub_date = now

                image_url = None
                if feed_type == "RSS":
                    if hasattr(item, "enclosure") and item.enclosure:
                        for enclosure in item.enclosure:
                            enclosure_type = enclosure.attributes.get("type", "")
                            if enclosure_type.startswith("image/"):
                                image_url = enclosure.attributes.get("url")
                                break
                elif feed_type == "Atom":
                    if hasattr(item, "media_groups") and item.media_groups:
                        for media_group in item.media_groups:
                            for thumbnail in media_group.thumbnails:
                                image_url = thumbnail.attributes.get("url")
                                if image_url:
                                    break

                existing_article = Article.objects.filter(
                    medium=medium,
                    guid=guid,
                    title=title,
                    description=description,
                    url=url,
                    published_at=pub_date,
                ).first()

                if existing_article:
                    self.stdout.write(f"     > exists: {existing_article.id}")
                    self.update_article_image_url(existing_article, image_url)
                    continue

                article, created = Article.objects.update_or_create(
                    medium=medium,
                    guid=guid,
                    defaults={
                        "title": title,
                        "description": description,
                        "url": url,
                        "published_at": pub_date,
                    },
                )

                action_text = "created" if created else "updated"
                self.stdout.write(f"     > {action_text}: {article.id}")
                self.update_article_image_url(article, image_url)

        except DontRetryException:
            self.stdout.write(f"   > error: DontRetryException")
            self.stdout.write("")
            return
        except Exception as e:
            with push_scope() as scope:
                scope.set_extra("command", "parse_articles")
                scope.set_extra("rss_url", url)
                capture_exception(e)
            self.stderr.write(self.style.ERROR(f"   > error: {e}"))
            self.stderr.write("")
            return

        self.stdout.write("")

    def handle(self, *args, **options):
        self.stdout.write("Starting ...")

        media = Medium.objects.all()
        for medium in media:
            self.stdout.write(f"Medium: {medium}")

            rss_urls = medium.article_rss_urls.split("\n")
            rss_urls = [
                rss_url.strip() for rss_url in rss_urls if rss_url and rss_url.strip()
            ]

            for rss_url in rss_urls:
                self.parse_rss_feed(medium, rss_url)

            self.stdout.write("")

        self.stdout.write("Done")
