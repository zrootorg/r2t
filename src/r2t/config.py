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
import yaml
import threading
from typing import Dict


class Config(object):
    __map: Dict

    def __init__(self) -> None:
        self.__map = {}
        self.lock = threading.Lock()

    def fromFile(self, filename: str) -> bool:
        if filename is None:
            return False
        try:
            with open(filename) as c:
                validyaml = yaml.safe_load(c)
                self.lock.acquire()
                m = validyaml
                if m:
                    self.__map = m
                self.lock.release()
        except (ValueError, TypeError, FileNotFoundError) as e:
            logging.error(f"exception {e}")
            return False
        return True

    def __iter__(self):
        for p in self.__map:
            yield p

    def __str__(self) -> str:
        return str(self.__map)

    def __getitem__(self, item):
        if item not in self.__map:
            raise KeyError
        try:
            self.lock.acquire()
            return self.__map[item]
        finally:
            self.lock.release()

    def __getattr__(self, item):
        try:
            self.lock.acquire()
            if item in self.__map:
                return self.__map[item]
        finally:
            self.lock.release()

    def add(self, item, value):
        try:
            self.lock.acquire()
            self.__map[item] = value
        except (ValueError, TypeError) as e:
            logging.error(f"Cannot add {item}={value}:  {e}")
            return False
        finally:
            self.lock.release()


cfg = Config()
