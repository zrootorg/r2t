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
import time

class Parser(object):
    feeds: List = list()
    db: DB = None

    def __init__(self, feeds:List[Dict[str,str]], db: DB)-> None:
        self.feeds = feeds
        self.db = db

    def list_feeds(self):
        return self.feeds

    def parse(self):
      for feed, url in self.feeds.items():
            self.db.create_table(feed)
            parsed_feed = feedparser.parse(url)
            for article in sorted(
                parsed_feed["entries"], key=lambda k: k.published, reverse=False
            ):
                if self.db.is_found(feed, article["title"], article["update"]):
                    continue
                self.db.add_item(feed, article["title"], article["update"])
                # TODO: send message to telegram
                time.sleep(5) # wait a bit to avoid telegram ban

    def run(self):
        # make it multi-threaded
        pass
    def stop():
        # make it multi-threaded
        pass
