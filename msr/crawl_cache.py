import click
import json
import sqlite3
import time
import os
from pathlib import Path
from urllib.parse import urlparse


class CrawlCache:
    @staticmethod
    def create(base_dir):
        """Optionally create the DB file, and return the registry"""
        db_file = f"{base_dir}/msr-cache.db"
        if not os.path.exists(db_file):
            Path(base_dir).mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(db_file)
            conn.cursor().execute('''
            CREATE TABLE link_cache(
             url text PRIMARY KEY,
             links text,
             cacheExpiryTime integer
            )''')
            conn.close()
        return CrawlCache(sqlite3.connect(db_file))

    def __init__(self, conn):
        self.conn = conn

    def add_link(self, url, links, cacheTime):
        cacheExpiryTime = int(time.time()) + cacheTime
        serialized_links = json.dumps(links)
        self.conn.cursor().execute(
            f"INSERT OR IGNORE into link_cache (url, links, cacheExpiryTime) values (?, ?, ?)",
            (url, serialized_links, cacheExpiryTime))
        self.conn.commit()

    def cached_children(self, url):
        """Returns the list of cached links if any, otherwise returns None"""
        for row in self.conn.cursor().execute(
                "SELECT * from link_cache where url = ?", [url]):
            url, raw_links, cacheExpiryTime = row
            if cacheExpiryTime > int(time.time()):
                return json.loads(raw_links)
        return None
