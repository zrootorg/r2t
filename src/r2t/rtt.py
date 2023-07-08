#!/usr/bin/env python
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

"""
RTT: Telegram Feed Reader
"""

import sqlite3
import time
import os
import logging
import yaml

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

try:
    import feedparser
    import telegram
except ModuleNotFoundError:
    logging.error("Module not found, please install")


def db_create(dbname):
    db.execute("CREATE TABLE IF NOT EXISTS " + dbname + "(title TEXT, date TEXT)")


def article_not_db(article_title, article_date, feed):
    db.execute(
        "SELECT * from " + feed + " WHERE title=? AND date=?",
        (article_title, article_date),
    )
    if not db.fetchall():
        return True
    else:
        return False


def add_article_to_db(article_title, article_date, feed):
    db.execute("INSERT INTO " + feed + " VALUES (?,?)", (article_title, article_date))
    db_connection.commit()


def bot_send_msg(chatid, feed, title, link):
    bot.send_message(
        chat_id=chatid,
        text=f"<code>🆕 {feed} </code>\n\n<b>{title}</b>\n\n{link}",
        disable_web_page_preview=False,
        parse_mode="Html",
    )


def main():
    while True:
        for feed, url in rtt_settings["feed"].items():
            logging.info(f"Parsing: {feed}, {url}")
            parsed_feed = feedparser.parse(url)
            db_create(feed)
            for a in sorted(
                parsed_feed["entries"], key=lambda k: k.published, reverse=False
            ):
                if article_not_db(a["title"], a["updated"], feed):
                    logging.info(f"Sending new feed: {a['title']} - {a['link']}")
                    add_article_to_db(a["title"], a["updated"], feed)
                    bot_send_msg(
                        os.environ["TGCHATID"],
                        feed,
                        a["title"],
                        a["link"],
                    )
                    time.sleep(10)
                    continue
                else:
                    time.sleep(5)


if __name__ == "__main__":
    with open(os.getenv("CONFIGFILE", "/usr/src/app/settings.yaml")) as cfg:
        rtt_settings = yaml.safe_load(cfg)
    bot = telegram.Bot(token=os.environ['TGTOKEN'])
    db_connection = sqlite3.connect(os.getenv("DBFILE", "/tmp/rtt.sqlite"))
    db = db_connection.cursor()
    logging.info("Starting..")
    main()
    db_connection.close()
    logging.info("Goodbye..")
