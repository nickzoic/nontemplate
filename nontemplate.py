#!/usr/bin/env python
""" nontemplate is not a templating language """

class Element:
    """ An element within a nontemplate document """
    document = None
    tag_name = None
    element = None
    
    def __init__(self, document, tag_name):
        self.document = document
        self.tag_name = tag_name 
        
    def __call__(self, *args, **kwargs):
        self.element = lxml.etree.Element(self.tag_name, **kwargs)
        return self
    
    def __enter__(self):
        self.document._enter(self)
    
    def __exit__(self, type, value, tb):
        self.document._exit(self)

    def open_tag(self):
        return "<%s>" % self.tag_name
    
    def close_tag(self):
        return "</%s>\n" % self.tag_name
    
class Document:
    """ A nontemplate document ... emits XML """
    
    def __init__(self, output):
        self._output = output or ""
    
    def _emit(self, text):        
        if type(self._output) is str:
            self.output += text
        elif type(self._output) is list:
            self._output.append(text)
        else:
            self._output(text)
    
    def _enter(self, element):
        self._emit(element.open_tag())
    
    def _exit(self, element):
        self._emit(element.close_tag())
    
    def __getattr__(self, name):
        return Element(self, name)

    def __repr__(self):
        return "nontemplate Document Instance"
    
    def __str__(self):
        return self._output
    

