import sys

from whoosh import index
ix = index.open_dir("indexdir")

writer = ix.writer()
writer.update_document(path=u'PMZ_0004470-RA', content=u'titus rocks')
writer.commit()
