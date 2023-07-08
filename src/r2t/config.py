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
        return self.__map[item]

    def __getattr__(self, item):
        if item in self.__map:
            return self.__map[item]

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
