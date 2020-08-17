import requests

from html.parser import HTMLParser
from urllib.parse import urlparse


class Crawler:
    def __init__(self, cache, max_depth=2):
        self.max_depth = max_depth
        self.cache = cache

    def crawl(self, url):
        """Return this child links of this URL"""
        return self.__crawl_link(url, self.max_depth)

    def __crawl_link(self, url, depth):
        print(f"Crawling {url} at depth {depth}")
        if depth <= 0:
            return []

        all_links = self.__children(url)

        for link in all_links:
            all_links = all_links + self.__crawl_link(link, depth - 1)

        return all_links

    def __children(self, url):
        cached_links = self.cache.cached_children(url)

        if cached_links or cached_links == []:
            return cached_links

        response = requests.get(url)
        parser = AnchorParser(url)
        parser.feed(response.text)
        links = parser.links

        self.cache.add_link(url, links, 30 * 60)
        return links


class AnchorParser(HTMLParser):
    def __init__(self, url):
        super().__init__()
        self.links = []
        self.url = urlparse(url)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            [
                self.links.append(link) for (key, link) in attrs
                if key == 'href' and urlparse(link).scheme
            ]

    def build_link_url(self, link):
        parsed_link = urlparse(link)
        if not parsed_link.netloc:
            parsed_link.netloc = self.url.netloc

        if not parsed_link.scheme:
            parsed_link.scheme = self.url.scheme

        if parsed_link.path and parsed_link.path[0] != '/':
            parsed_link.path = self.url.path + parsed_link.path

        parsed_link.geturl()
