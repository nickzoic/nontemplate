#!/usr/bin/env python
# nontemplate.py
# Copyright (c) 2010 Nick Moore <nick@zoic.org>

import re


try:
    from cStringIO import StringIO     # Python 2
except ImportError:
    from io import StringIO            # Python 3


# Useful DOCTYPE_* strings for use with Document._doctype()

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
    
    '''Escapes & < > ... probably should handle unicode as well, translate
    it into HTML unicode entities.'''

    return re.sub(r'([&<>])', lambda match: HTML_ESCAPE_ENTITIES[match.group(0)], text)


def comment_escape(text):
    
    '''Escapes --> in a comment, because that's the only thing we really
    have to escape in a comment!'''

    return re.sub(r'-->', '-- >', text)



      

class Document(object):

    '''keeps track of the state of a NonTemplate XML document.
    See http://code.zoic.org/nontemplate/ for details.'''

    _intag = None
    _stack = []
    
    def __init__(self, output=None):
       
        '''`output` is something which can be written to with .write().
        Defaults to a new StringIO(), you can get the content out by 
        calling str() on the Document object'''

        self._output = output or StringIO()

    
    def _emit(self, s):

        '''Emit raw text into the output.  Used internally, also can
        be used if you need to break some XHTML rules.'''

        self._output.write(s)


    def _text(self, s):

        '''Emit some text, escaping < and > and &'''

        self._emit(html_escape(s)+"\n")


    def _comment(self, s):

	'''Convenience method for emitting comments.  Escapes "-->"
        into "-- >"'''

        self._emit("<!-- " + comment_escape(s) + " -->\n")


    def _doctype(self, doctype):
 
        '''Convenience method for emitting the doctype.  There's 
        a bunch of handy constants declared up there'''

        self._emit("<!DOCTYPE " + (' '.join(doctype)) + ">\n")


    def __getattr__(self, name):

	'''When we we're called with any other method, eg: a tag,
        this makes up a method to handle it, memoizes it in the class,
        and then call it on the instance.'''
        
        def newtagmethod(self, **kwargs):
            if self._intag:
                self._emit("/>\n<" + name)
            else:
                self._emit('<' + name)
            if kwargs:
                for k,v in kwargs.iteritems():
                    self._emit(' %s="%s"' % (
                        k[1:] if k[0] == '_' else k, html_escape(v)
                    ))
            self._intag = name
            return self
        
        setattr(self.__class__, name, newtagmethod)
        return getattr(self, name)

    
    def __call__(self, *args):

        '''Handy shortcut for putting some content in a tag'''
	
        if self._intag:   
            self._emit(">\n")
	for text in args:
	    self._text(text)
        if self._intag:
	    self._emit("</%s>\n" % self._intag)
	    self._intag = None


    def __enter__(self):

        '''The 'with' finishes the tag, and pushes the tag's name onto
        the stack so it'll be there when we __exit__'''

        self._emit(">\n")
        self._stack.append(self._intag)
        self._intag = None


    def __exit__(self, *stuff):

        '''At the end of the 'with', pop the latest tag off and close it.'''

        self._emit("</" + self._stack.pop() + ">\n")
        return False 


    def __str__(self):

        '''If you initialize the object with a StringIO (or pass no 
        `output` parameter, thus getting one), this method can
        be used to get the text back'''

        return self._output.getvalue()
