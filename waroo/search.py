from whoosh import index
from whoosh.qparser import MultifieldParser

ix = index.open_dir("indexdir")

def do_search(q):
    q = q.replace(" and ", " AND ")
    q = q.replace(" or ", " OR ")
    q = q.replace(" not ", " NOT ")
    
    searcher = ix.searcher()
    query = MultifieldParser(["oneline","content", "acc"]).parse(q)
    results = searcher.search(query, limit=None)

    return [ (r['acc'], r['oneline']) for r in results ]

def update_record(acc, oneline, content):
    writer = ix.writer()
    writer.update_document(acc=unicode(acc),
                           oneline=unicode(oneline),
                           content=unicode(content))
    writer.commit()
