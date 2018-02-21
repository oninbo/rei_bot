import shelve
import os.path

db_path = 'data/quote_db'


def set_quote_db():
    quote_db = shelve.open(db_path)
    quote_db['list'] = []
    quote_db.close()


def add_to_quote_db(item):
    if not os.path.isfile(db_path):
        set_quote_db()
    quote_db = shelve.open(db_path)
    list = quote_db['list']
    for i in list:
        if i.value == item.value:
            quote_db.close()
            return
    list.append(item)
    quote_db['list'] = list
    quote_db.close()


def remove_from_quote_db(item):
    if not os.path.isfile(db_path):
        set_quote_db()
    quote_db = shelve.open(db_path)
    list = quote_db['list']
    for i in list:
        if i.value == item.value:
            list.remove(i)
    quote_db['list'] = list
    quote_db.close()


def get_quote_db_list():
    if not os.path.isfile(db_path):
        set_quote_db()
    quote_db = shelve.open(db_path)
    list = quote_db['list']
    quote_db.close()
    return list