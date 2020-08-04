import sqlite3
import os
from pathlib import Path

class Registry:
  @staticmethod
  def create(base_dir):
    """Optionally create the DB file, and return the registry"""
    db_file = f"{base_dir}/msr.db"
    if not os.path.exists(db_file):
      Path(base_dir).mkdir(parents=True, exist_ok=True)
      conn = sqlite3.connect(db_file)
      conn.cursor().execute('''CREATE TABLE urls (url text)''')
      conn.close()
    return Registry(sqlite3.connect(db_file))

  def __init__(self, conn):
    self.conn = conn

  def register(self, url):
    """Adds the URL to the registry"""
    self.conn.cursor().execute(f"INSERT into urls (url) values (?)", (url,))
    self.conn.commit()

  def list(self):
    """Returns an iterator of all URLs in the registry"""
    for row in self.conn.cursor().execute("SELECT url from urls"):
      yield row[0]