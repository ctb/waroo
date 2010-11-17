# -*- coding: iso-8859-1 -*-
import os.path
from optparse import OptionParser
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler
from quixote.server.simple_server import run as run_simple_server

import pkg_resources
pkg_resources.require('quixote >= 2.6')
pkg_resources.require('jinja2')

import quixote
from quixote.directory import Directory
from quixote.publish import Publisher
from quixote.util import StaticDirectory

import jinja2

###

from . import db, search

#from . import tags, objects, db, search

### set up jinja templates

thisdir = os.path.dirname(__file__)
templatesdir = os.path.join(thisdir, 'templates')
templatesdir = os.path.abspath(templatesdir)

loader = jinja2.FileSystemLoader(templatesdir)
env = jinja2.Environment(loader=loader)

def render_jinja2(t, d):
    e = {}
    for k, v in d.items():
        if isinstance(v, str):
            e[k] = unicode(v)
        else:
            e[k] = v

    return t.render(e)

###

class TopDirectory(Directory):
    _q_exports = ['', 'css', 'tiny_mce', 'display', 'edit', 'search', 'save']
    
    css = StaticDirectory(os.path.join(templatesdir, 'css'), use_cache=True)
    tiny_mce = StaticDirectory(os.path.join(templatesdir, 'tiny_mce'),
                               use_cache=True)

    def _q_index(self):
        id = "foo"
        oneline = "bar"
        annot = "bif"
        
        template = env.get_template('index.html')
        return render_jinja2(template, locals())

    def search(self):
        request = quixote.get_request()
        form = request.form

        q = form['q'].strip()
        results = search.do_search(q)

        template = env.get_template('search_results.html')
        return render_jinja2(template, locals())

    def display(self):
        request = quixote.get_request()
        form = request.form
        
        acc = form['acc']
        oneline, content = db.get_gene(acc)

        template = env.get_template('display.html')
        return render_jinja2(template, locals())

    def edit(self):
        request = quixote.get_request()
        form = request.form
        
        acc = form['acc']
        oneline, content = db.get_gene(acc)

        template = env.get_template('edit.html')
        return render_jinja2(template, locals())

    def save(self):
        request = quixote.get_request()
        form = request.form
        
        acc = form['acc']
        oneline = form['oneline']
        content = form['content']

        db.update_gene(acc, oneline, content)
        search.update_record(acc, oneline, content)
        
        return request.response.redirect(str(request.get_url(1) + '/display?acc=%s' % acc))

def create_publisher():
    # sets global Quixote publisher
    Publisher(TopDirectory(), display_exceptions='plain')

    # return a WSGI wrapper for the Quixote Web app.
    app = quixote.get_wsgi_app()
    app.publisher.is_thread_safe = True
    return app

def run_wsgi(port=8123):
    server = WSGIServer(('', port), WSGIRequestHandler)
    app = create_publisher()
    server.set_app(app)

    print 'serving on %s:%d' % (interface, port,)
    server.serve_forever()

def run(interface, port):
    print 'serving on %s:%d' % (interface, port,)
    run_simple_server(create_publisher, interface, port)


if __name__ == '__main__':
    import sys
    parser = OptionParser()

    parser.add_option('-i', '--interface', dest='interface',
                      help='interface to bind', default='localhost')
    parser.add_option('-p', '--port', dest='port', help='port to bind',
                      type='int', default='8123')
    
    (options, args) = parser.parse_args()

    ##

    run(options.interface, options.port)
