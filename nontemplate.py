# nontemplate.py
# Copyright (c) 2010 Nick Moore <nick@zoic.org>

DOCTYPE_HTML_2_0 = ['HTML', 'PUBLIC', '"-//IETF//DTD HTML//EN"']
DOCTYPE_HTML_3_2 = ['HTML', 'PUBLIC', '"-//W3C//DTD HTML 3.2 Final//EN"']
DOCTYPE_HTML_4_01_STRICT = ['HTML', 'PUBLIC', '"-//W3C//DTD HTML 4.01//EN"', '"http://www.w3.org/TR/html4/strict.dtd"']
DOCTYPE_HTML_4_01_TRANSITIONAL = ['HTML', 'PUBLIC', '"-//W3C//DTD HTML 4.01 Transitional//EN"', '"http://www.w3.org/TR/html4/loose.dtd"']
DOCTYPE_HTML_4_01_FRAMESET = ['HTML', 'PUBLIC', '"-//W3C//DTD HTML 4.01 Frameset//EN"', '"http://www.w3.org/TR/html4/frameset.dtd"']
DOCTYPE_XHTML_1_STRICT = ['html','PUBLIC','"-//W3C//DTD XHTML 1.0 Strict//EN"', '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"']
DOCTYPE_XHTML_1_TRANSITIONAL = ['html', 'PUBLIC', '"-//W3C//DTD XHTML 1.0 Transitional//EN"','"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"']
DOCTYPE_XHTML_1_FRAMESET = ['html', 'PUBLIC', '"-//W3C//DTD XHTML 1.0 Frameset//EN"', '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd"']
DOCTYPE_HTML_5 = ['html']


HTML_ESCAPE_ENTITIES = { '<': '&lt;', '>': '&gt;', '&': '&amp;' }

def html_escape(text):
    return ''.join((
        HTML_ESCAPE_ENTITIES.get(c, str(c)) if 32 <= ord(c) < 128 else "&#%d;" % ord(c)
        for c in text
    ))

class Document:

    _output = None
    _intag = None
    _stack = []

    def __init__(self, output=None):
        self._output = output

    def _emit(self, s):
        self._output.write(s) 

    def _text(self, s):
        self._emit(html_escape(s)+"\n")

    def _comment(self, s):
        self._emit("<!-- " + html_escape(s) + " -->\n")

    def _doctype(self, *stuff):
        self._emit("<!DOCTYPE " + (' '.join(stuff)) + ">\n")

    def __getattr__(self, name):
        if self._intag:
            self._emit("/>\n")
        self._emit("<%s" % name)
        self._intag = name
        return self

    def __call__(self, arg0=None, **kwargs):
        if arg0 and not self._intag:
            self._emit("<%s" % arg0)

        for k,v in kwargs.iteritems():
            self._emit(' %s="%s"' % (k[1:] if k[0] == '_' else k, html_escape(v)))

        if arg0:
            if self._intag:
                self._emit(">%s</%s>\n" % (html_escape(arg0), self._intag))
                self._intag = None
            else:
                self._intag = arg0

        return self

    def __enter__(self):
        self._emit(">\n")
        self._stack.append(self._intag)
        self._intag = None

    def __exit__(self, *stuff):
        self._emit("</%s>\n" % self._stack.pop())
        return False 


#-----

import sys

data = [
    [ str(x * 10 + y + 1) for y in range(0,10) ]
    for x in range(0,100)
]

def runme():
    for z in range(0,1000):
        D = Document(sys.stdout)
        with D.table:
            for a in data:
                with D.tr:
                    for b in a:
                        with D.td:
                            D._emit(b)

import cProfile
cProfile.run('runme()','profile')

import pstats
p = pstats.Stats('profile')
p.sort_stats('cumulative').print_stats()