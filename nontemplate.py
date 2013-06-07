#!/usr/bin/env python
# nontemplate.py
# Copyright (c) 2010 Nick Moore <nick@zoic.org>

import re
from xml.sax.saxutils import escape, quoteattr

try:
    from cStringIO import StringIO     # Python 2
except ImportError:
    from io import StringIO            # Python 3


class doctype:
    '''Doctypes for nontemplate documents'''
    html_2_0 = 'HTML PUBLIC "-//IETF//DTD HTML//EN"'
    html_3_2 = 'HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"'
    html_4_01_strict = 'HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"'
    html_4_01_transitional = 'HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"'
    html_4_01_frameset = 'HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd"'
    xhtml_1_strict = 'html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"'
    xhtml_1_transitional = 'html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"'
    xhtml_1_frameset = 'html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd"'
    html_5 = 'html'



class Document(object):

    '''keeps track of the state of a NonTemplate XML document.
    See http://code.zoic.org/nontemplate/ for details.'''

    # XXX probably should track doctype so as to tweak the output to suit that doctype better.
    # or maybe have subclasses which specialize Document to cope with that?
    
    _intag = None
    _stack = []


    def __init__(self, output=None, doctype=None):

        '''`output` is something which can be written to with .write().
        Defaults to a new StringIO(), you can get the content out by 
        calling str() on the Document object'''

        self._output = output or StringIO()
        if doctype:
            self._doctype(doctype)


    def _emit(self, s):

        '''Emit raw text into the output.  Used internally, also can
        be used if you need to break some XHTML rules.'''

        self._output.write(s)


    def _text(self, s):

        '''Emit some text, escaping < and > and &'''

        self._emit(escape(s)+"\n")


    def _attr(self, k, v):
        # handle 'modern' HTMLs insistence on 'foo="foo"' attributes by substituting booleans.
        # XXX not sure if this is a good idea.
        
        if v == True:
            self._emit(' %s="%s"' % (k,k))
        elif v == False:
            self._emit(' %s=""' % k)
        else:
            self._emit(' %s=%s' % (k, quoteattr(v)))

    
    def _comment(self, s):

        '''Convenience method for emitting comments.  Escapes "-->"
        into "-- >"'''

        self._emit("<!-- " + escape(s) + " -->\n")


    def _doctype(self, doctype):

        '''Convenience method for emitting the doctype.  There's 
        a bunch of handy constants declared up there'''

        self._emit("<!DOCTYPE %s>\n" % doctype)


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
                for k,v in kwargs.items():
                    self._attr(k[1:] if k[0] == '_' else k, v)
                    
            self._intag = name
            return self

        setattr(self.__class__, name, newtagmethod)
        return getattr(self, name)


    def __call__(self, *args):

        '''Handy shortcut for putting some content in a tag'''

        if self._intag:   
            self._emit(">\n")
        for text in args:
            self._text(str(text))
        if self._intag:
            self._emit("</%s>\n" % self._intag)
            self._intag = None
        return self


    def __enter__(self):

        '''The 'with' finishes the tag, and pushes the tag's name onto
        the stack so it'll be there when we __exit__'''

        if self._intag:
            self._emit(">\n")
        self._stack.append(self._intag)
        self._intag = None


    def __exit__(self, *stuff):

        '''At the end of the 'with', pop the latest tag off and close it.'''
        
        if self._intag:
            self._emit("/>\n")
        self._emit("</" + self._stack.pop() + ">\n")
        self._intag = None
        return False 


    def __str__(self):

        '''If you initialize the object with a StringIO (or pass no 
        `output` parameter, thus getting one), this method can
        be used to get the text back'''

        return self._output.getvalue()
