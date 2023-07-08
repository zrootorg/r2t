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
import sqlite3

class DB(object):
    def __init__(self, path:str) -> None:
        self.db_conn = sqlite3.connect(path)
        self.db = self.db_conn.cursor()
        pass

    def create_table(self, table: str) -> bool:
        cur = self.db.execute("CREATE TABLE IF NOT EXISTS ? (title text, date text)", (table))
        res = cur.fetchone()
        if res is None:
            return False
        return True

    def is_found(self, table: str, title: str, date: str) -> bool:
        cur = self.db.execute("SELECT * from ? WHERE title=? AND date=?", (table, title, date))
        if not cur.fetchall():
            return False
        return True

    def add_item(self, table: str, title: str, date: str) -> None:
        self.db.execute("INSERT INTO ? VALUES (?,?)", (table, title, date))
        self.db_conn.commit()
