import time

import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_datetime
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.core.validators import URLValidator
from django.utils import timezone
from django.utils.html import strip_tags
from meta_tags_parser.parse import parse_meta_tags_from_source
from meta_tags_parser.structs import SettingsFromUser, WhatToParse
from rss_parser import AtomParser, RSSParser, detect_feed_type, FeedType
from sentry_sdk import capture_exception, capture_message, push_scope

from ...models import Article, Medium


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
            options=SettingsFromUser(
                what_to_parse=(WhatToParse.OPEN_GRAPH, WhatToParse.TWITTER),
            ),
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

        self.stdout.write(f" > feed url: {url}")

        try:
            time.sleep(3)  # wait to avoid rate limiting
            response = requests_get_with_retries(url, timeout=30)

            content_type = response.headers.get("Content-Type", "").lower()
            if "xml" not in content_type:
                raise ValueError(f"Unexpected content type: {content_type}")

            response_text = response.text
            feed_type = detect_feed_type(response_text)
            if feed_type == FeedType.ATOM:
                rss = AtomParser.parse(response_text)
                feed_title = rss.feed.title.content
                items = rss.feed.entries
            elif feed_type == FeedType.RSS:
                rss = RSSParser.parse(response_text)
                feed_title = rss.channel.title.content
                items = rss.channel.items
            else:
                raise ValueError(f"Unsupported feed type: {feed_type}")

            self.stdout.write(f"   > feed type: {feed_type}")
            self.stdout.write(f"   > title: {feed_title}")
            self.stdout.write(f"   > found items: {len(items)}")
            self.stdout.write("")

            for item in items:
                title = item.title.content
                if len(title) > 256:
                    title = title[:253] + "..."

                self.stdout.write(f"   > {title[:67]}")

                link = item.links[0] if len(item.links) else None
                if feed_type == FeedType.ATOM:
                    link_content = link.attributes.get("href", None) if link else None
                elif feed_type == FeedType.RSS:
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
                    continue

                url = link_content[:512]
                description = ""
                if feed_type == FeedType.RSS:
                    if item.description and item.description.content:
                        description = strip_tags(item.description.content)
                elif feed_type == FeedType.ATOM:
                    if item.summary and item.summary.content:
                        description = strip_tags(item.summary.content)
                    elif item.content and item.content.content:
                        description = strip_tags(item.content.content)
                    elif mg := item.content.model_extra.get("media:group", None):
                        if md := mg.get("media:description", None):
                            description = strip_tags(md)
                if len(description) > 256:
                    description = description[:253] + "..."

                if feed_type == FeedType.RSS:
                    guid = item.guid.content if item.guid else None
                elif feed_type == FeedType.ATOM:
                    guid = item.id.content if item.id else None

                if not guid:
                    guid = link_content
                if not guid:
                    guid = item.title.content
                if guid and len(guid) > 256:
                    guid = guid[:253] + "..."

                if feed_type == FeedType.RSS:
                    pub_date = item.pub_date.content if item.pub_date else None
                elif feed_type == FeedType.ATOM:
                    pub_date = item.published.content if item.published else None

                if pub_date and isinstance(pub_date, str):
                    pub_date = parse_datetime(pub_date)
                if not pub_date:
                    pub_date = now

                image_url = None
                if feed_type == FeedType.RSS:
                    for enclosure in item.enclosures:
                        enclosure_type = enclosure.attributes.get("type", "")
                        if enclosure_type.startswith("image/"):
                            image_url = enclosure.attributes.get("url")
                            break
                elif feed_type == FeedType.ATOM:
                    if mg := item.content.model_extra.get("media:group", None):
                        if mt := mg.get("media:thumbnail", None):
                            image_url = mt.get("@url", None)

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
