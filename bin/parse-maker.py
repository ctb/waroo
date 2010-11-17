#! /usr/bin/env python
import screed, sys
import sqlite3
from screed.fasta import fasta_iter

db = sqlite3.connect('test.db')
c = db.cursor()

c.execute('CREATE TABLE genes (id INTEGER PRIMARY KEY, acc TEXT, oneline TEXT, content TEXT)');

from whoosh.index import create_in
from whoosh.fields import *
schema = Schema(acc=ID(stored=True,unique=True), oneline=TEXT(stored=True),
                content=TEXT)
ix = create_in("indexdir", schema)
writer = ix.writer()

for record in fasta_iter(open(sys.argv[1])):
    acc = record['name']
    descr = record['description']
    idx = descr.find(' Name:')
    idx2 = descr.find('" ', idx)
    assert idx > 0
    assert idx2 > 0

    descr = descr[idx + 7:idx2]
    print acc, descr
    writer.add_document(acc=unicode(acc), oneline=unicode(descr))

    c.execute('INSERT INTO genes (acc, oneline, content) VALUES (?, ?, ?)', (acc, descr, ''))

writer.commit()
db.commit()

