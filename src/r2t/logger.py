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
import logging
from loguru import logger
from prometheus_client import Counter
import urllib3

error_counter = Counter("rt2_error_counter", "Number of errors", ["error_type"])


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 7
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        error_counter.labels(record.levelname).inc()
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())



def setup_logger(level: str = "info"):
    urllib3.disable_warnings()
    levels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR
        }
    # setting the standard logger to use loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=levels[level.lower()])
