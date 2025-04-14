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
from rss_parser import Parser
from rss_parser.models import XMLBaseModel
from rss_parser.models.channel import Channel
from rss_parser.models.item import Item
from rss_parser.models.rss import RSS
from rss_parser.models.types.only_list import OnlyList
from rss_parser.models.types.tag import Tag
from rss_parser.pydantic_proxy import import_v1_pydantic
from sentry_sdk import capture_exception, capture_message, push_scope

from ...models import Article, Medium

pydantic = import_v1_pydantic()


# Fix for rss_parser pydantic validation error on multiple categories
class CustomItem(Item):
    category: Optional[OnlyList[Tag[str]]] = None
    enclosure: Optional[OnlyList[Tag[str]]] = None


class CustomChannel(Channel, XMLBaseModel):
    items: Optional[OnlyList[Tag[CustomItem]]] = pydantic.Field(
        alias="item",
        default=[],
    )


class CustomSchema(RSS, XMLBaseModel):
    version: Optional[Tag[str]] = pydantic.Field(alias="@version")
    channel: Tag[CustomChannel]


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
            response = requests.get(article.url, timeout=10)
            response.raise_for_status()
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

    def parse_rss_feed(self, medium, url):
        now = timezone.now()

        self.stdout.write(f" > rss url: {url}")

        try:
            time.sleep(3)  # wait to avoid rate limiting
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            response_text = response.text
            # fix random problems with rss feeds
            response_text = response_text.replace("<title>&nbsp;", "<title>")

            rss = Parser.parse(response_text, schema=CustomSchema)

            self.stdout.write(f"   > title: {rss.channel.title.content}")
            self.stdout.write(f"   > found items: {len(rss.channel.items)}")
            self.stdout.write("")

            for item in rss.channel.items:
                title = item.title.content
                if len(title) > 256:
                    title = title[:253] + "..."

                self.stdout.write(f"   > {title[:67]}")

                if (
                    item.link
                    and item.link.content
                    and not item.link.content.startswith("http")
                ):
                    if item.link.content.startswith("//"):
                        item.link.content = f"http:{item.link.content}"
                    if "://" not in item.link.content:
                        item.link.content = f"http://{item.link.content}"

                if not self.is_url(item.link.content):
                    with push_scope() as scope:
                        scope.set_extra("command", "parse_articles")
                        scope.set_extra("rss_url", url)
                        capture_message(f"Invalid url: {item.link.content}")
                    self.stdout.write(f"     > invalid url: {item.link.content}")
                    self.stdout.write("")
                    continue

                url = item.link.content[:512]

                description = strip_tags(item.description.content)
                if len(description) > 256:
                    description = description[:253] + "..."

                guid = item.guid.content if item.guid else None
                if not guid:
                    guid = item.link.content if item.link else None
                if not guid:
                    guid = item.title.content
                if guid and len(guid) > 256:
                    guid = guid[:253] + "..."

                pub_date = item.pub_date.content if item.pub_date else None
                if pub_date:
                    pub_date = parse_datetime(pub_date)
                else:
                    pub_date = now

                image_url = None
                if item.enclosure:
                    for enclosure in item.enclosure:
                        enclosure_type = enclosure.attributes.get("type", "")
                        if enclosure_type.startswith("image/"):
                            image_url = enclosure.attributes.get("url")
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
