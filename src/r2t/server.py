# -*- coding: utf-8 -*-
#
# This file is part of the pdh (https://github.com/mbovo/pdh).
# Copyright (c) 2016-2023 Manuel Bovo
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
import threading
import concurrent.futures
import sys
import time
import logging
import uvicorn
from .config import cfg
from .feedparser import Parser
from .db import DB

thread_pool: concurrent.futures.ThreadPoolExecutor
stop_event: threading.Event
server: uvicorn.Server
parser: Parser

def run():
    global thread_pool, stop_event
    functions = [webapp, feedparser]
    stop_event = threading.Event()
    thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=len(functions))
    future_tasks = {thread_pool.submit(fn): fn for fn in functions}
    for future in concurrent.futures.as_completed(future_tasks):
        future.result()

def stop():
    global thread_pool, stop_event, parser
    logging.info("signalling threads to stop")
    stop_event.set()
    server.should_exit = lambda: stop_event.is_set()
    thread_pool.shutdown(wait=False, cancel_futures=True)
    sys.exit(0)

def webapp():
    global server
    config = uvicorn.Config("r2t.api:app", port=int(cfg["port"]), log_level="error")
    server = uvicorn.Server(config)
    server.run()

def feedparser():
    global parser

    # Is very important to initialize the database and use it
    # in the same thread or sqlite will complain
    logging.info("Initializing database")
    database = DB(cfg["db_path"])

    logging.info("Starting feedparser")
    parser = Parser(cfg["feeds"], database, stop_event)
    while True:
        if stop_event.is_set():
            break
        parser.parse()
        logging.info(f"Sleeping for {cfg['refresh_time']} seconds")
        for i in range(0, int(cfg["refresh_time"])):
            if stop_event.is_set():
                break
            time.sleep(1)
    parser.stop()
