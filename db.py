import sqlite3
from sqlite3.dbapi2 import Cursor

conn = sqlite3.connect("blogs.sqlite")

cursor = conn.cursor()
sql_query = """ 
CREATE TABLE blog(
id integer PRIMARY KEY,
author text NOT NULL,
language text NOT NULL,
title text NOT NULL,
description text NOT NULL
)"""

cursor.execute(sql_query)
