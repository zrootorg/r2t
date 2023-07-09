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
import pkg_resources
import typer
import click
from pathlib import Path
from typing_extensions import Annotated
from typing import Optional
import logging
import signal
from . import logger
from . import server
from .config import cfg

app = typer.Typer()

@app.command()
def version():
    click.echo(f"v{pkg_resources.get_distribution('r2t').version}")

@app.command()
def start(tg_token: Annotated[str, typer.Option("--telegram-token", "-t", envvar="TELEGRAM_TOKEN", help="Telegram token")],
           tg_chat_id: Annotated[str, typer.Option("--telegram-chat-id", "-i", envvar="TELEGRAM_CHAT_ID", help="Telegram chat id")],
           port: Annotated[int, typer.Option("--port", "-p", envvar="PORT", help="Port")] = 5000,
           config: Annotated[Optional[Path], typer.Option("--config", "-c", envvar="CONFIG_FILE", help="Config file")] = "./config.yaml",
           log_level: Annotated[str, typer.Option("--log-level", "-l", envvar="LOG_LEVEL", help="Log level")] = "info",
           db_path: Annotated[str, typer.Option("--db-path", "-d", envvar="DB_PATH", help="SQLite db path")] = "./db.sqlite",
           refresh_time: Annotated[str, typer.Option("--refresh-time", "-r", envvar="REFRESH_TIME", help="RSS Feed refresh time (s)")] = 30,
           ):
    set_sig_handler(sig_handler)
    logger.setup_logger(log_level)
    logging.debug(f"Log level: {log_level}")
    if not (config.exists() and config.is_file()):
        click.echo(f"Config file {config} does not exist or is not a file")
        raise typer.Abort()
    logging.info(f"Using config file {config}")
    cfg.fromFile(config)
    cfg.add("port",port)
    cfg.add("tg_token",tg_token)
    cfg.add("tg_chat_id",tg_chat_id)
    cfg.add("db_path",db_path)
    cfg.add("refresh_time",refresh_time)
    logging.debug(f"Config: {cfg}")
    server.run()

def sig_handler(signum, stack):
    if signum in [1, 2, 3, 15]:
        logging.warning("Caught signal %s, exiting.", str(signum))
        server.stop()
    return stack


def set_sig_handler(funcname, avoid=["SIG_DFL", "SIGSTOP", "SIGKILL"]):
    for i in [x for x in dir(signal) if x.startswith("SIG") and x not in avoid]:
        try:
            signum = getattr(signal, i)
            signal.signal(signum, funcname)
        except (OSError, RuntimeError, ValueError) as m:  # OSError for Python3, RuntimeError for 2
            logging.warning("Skipping {} {}".format(i, m))


def main():
    app()
