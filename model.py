import web, datetime
#import sqlite3
import re

db = web.database(dbn="sqlite", db="qai")


def get_all_data_as_dict():
    rows = db.select('mdata')
    return {row.id: row for row in rows}
def insert_contact(name, email, subject, message):
    db.insert('contact', name=name, email=email, subject=subject, message=message)