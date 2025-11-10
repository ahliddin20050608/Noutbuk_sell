import sqlite3


def get_connect():
    return sqlite3.connect("db.sqlite3")
