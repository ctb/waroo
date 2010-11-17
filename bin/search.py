import sys

from whoosh import index
ix = index.open_dir("indexdir")

from whoosh.qparser import MultifieldParser
searcher = ix.searcher()
query = MultifieldParser(["oneline","content", "path"]).parse(sys.argv[1])
results = searcher.search(query, limit=100)
print len(results)
for r in results:
    print r['path'], r['oneline']


