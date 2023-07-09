# -*- coding: utf-8 -*-
#
# This file is part of the pdh (https://github.com/mbovo/pdh).
# Copyright (c) 2020-2023 Luigi Operoso, Manuel Bovo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from .db import DB
import feedparser
from typing import Dict,List
import threading
import logging

class Parser(object):
    feeds: List = list()
    db: DB = None

    def __init__(self, feeds:List[Dict[str,str]], db: DB, stop_event: threading.Event)-> None:
        self.feeds = feeds
        self.db = db
        self.stop_event = stop_event

    def list_feeds(self):
        return self.feeds

    def parse(self):
      logging.info("Start parsing feeds")
      for feed, url in self.feeds.items():
            logging.info(f"Parse feed {feed} {url}")
            if self.stop_event.is_set():
                logging.info("Stop event, quit")
                break
            self.db.create_table(feed)
            parsed_feed = feedparser.parse(url)
            for article in sorted(
                parsed_feed["entries"],
                key=lambda k: k.published,
                reverse=False
            ):
                if self.stop_event.is_set():
                    logging.info("Stop event, quit")
                    break
                if self.db.is_found(feed, article["title"], article["updated"]):
                    logging.info(f"Skip item {feed} {article['title']} {article['updated']}")
                    continue
                logging.info(f"Add item {feed} {article['title']} {article['updated']}")
                self.db.add_item(feed, article["title"], article["updated"])

    def stop(self):
        self.db.close()
        pass
