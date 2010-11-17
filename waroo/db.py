# -*- coding: iso-8859-1 -*-
import sqlite3

db = sqlite3.connect('test.db')

def get_gene(acc):
    c = db.cursor()
    c.execute('SELECT oneline,content FROM genes WHERE acc=?', (acc,))

    oneline, content = c.fetchone()
    return oneline, content

def update_gene(acc, oneline, content):
    c = db.cursor()
    c.execute('UPDATE genes SET oneline=?,content=? where acc=?',
              (oneline, content, acc))
    db.commit()
