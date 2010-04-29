#!/usr/bin/env python
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

# a very small list of entities to escape
HTML_ESCAPE_ENTITIES = { '<': '&lt;', '>': '&gt;', '&': '&amp;' }

import re

def html_escape(text):
    return re.sub(r'([&<>])', lambda match: HTML_ESCAPE_ENTITIES[match.group(0)], text)

def comment_escape(text):
    return re.sub(r'-->', '-- >', text)

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
      

class Document(object):

    _intag = None
    _stack = []
    
    def __init__(self, output=None):
        self._output = output or StringIO()
    
    def _emit(self, s):
        self._output.write(s)

    def _text(self, s):
        self._emit(html_escape(s)+"\n")

    def _comment(self, s):
        self._emit("<!-- " + comment_escape(s) + " -->\n")

    def _doctype(self, doctype):
        self._emit("<!DOCTYPE " + (' '.join(doctype)) + ">\n")

    def __getattr__(self, name):
        def newtagmethod(self, *args, **kwargs):
            if self._intag:
                self._emit("/>\n<" + name)
            else:
                self._emit('<' + name)
            if kwargs:
                for k,v in kwargs.iteritems():
                    self._emit(' %s="%s"' % (k[1:] if k[0] == '_' else k, html_escape(v)))
            if args:
	        self._emit(">\n")
		for a in args:
		    self._text(a)
		self._emit("</%s>\n" % name)
	        self._intag = None
	        return None
	    else:
                self._intag = name
            	return self
        
        setattr(self.__class__, name, newtagmethod)
        return getattr(self, name)
    
    def __call__(self, text):
        if self._intag:
	    self._emit(">\n")
	    self._text(text)
	    self._emit("</%s>\n" % self._intag)
	    self._intag = None
	    return None
	else:
	    self._text(text)
            return self

    def __enter__(self):
        self._emit(">\n")
        self._stack.append(self._intag)
        self._intag = None

    def __exit__(self, *stuff):
        self._emit("</" + self._stack.pop() + ">\n")
        return False 

    def __str__(self):
        return self._output.getvalue()
