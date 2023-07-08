import threading
import concurrent.futures
import sys
import logging
import uvicorn
from .config import cfg

thread_pool: concurrent.futures.ThreadPoolExecutor
stop_event: threading.Event
server: uvicorn.Server

def run():
    global thread_pool, stop_event
    functions = [webapp]
    stop_event = threading.Event()
    thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=len(functions))
    future_tasks = {thread_pool.submit(fn): fn for fn in functions}
    for future in concurrent.futures.as_completed(future_tasks):
        future.result()

def stop():
    global thread_pool, stop_event
    logging.info("signalling threads to stop")
    stop_event.set()
    server.should_exit = lambda: stop_event.is_set()
    thread_pool.shutdown(wait=False, cancel_futures=True)
    sys.exit(0)

def webapp():
    global server
    config = uvicorn.Config("r2t.api:app", port=int(cfg["port"]), log_level="info")
    server = uvicorn.Server(config)
    server.run()
