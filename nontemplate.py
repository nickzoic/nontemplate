#!/usr/bin/env python

class DocumentTag:
    
    name = None
    attrs = {}
    elems = []
    
    def __init__(self, document, name):
        self.name = name
        self.document = document
        self.tagged = False
        
    def __call__(self, *args, **kwargs):
        self.attr = kwargs
        
        for a in args:
            if type(a) is dict:
                self.attrs.update(a)
            elif type(a) in (unicode, str):
                self.elems.append(a)
            elif type(a) in (list, tuple):
                self.elems += str(a)
            else:
                self.elems += a.elems
            
        return self
    
    def __enter__(self):
        if not self.tagged:
            self.document._tag(self.name)
            self.tagged = True
        self.document._rewind()
            
    def __exit__(self, type, value, tb):
        self.document._forward()

    def __str__(self):
        return ( ("<%s" % self.name ) +
            ''.join([ '%s="%s"' % x for x in self.attrs.iteritems() ]) +
            ">" +
            ''.join(self.elems) +
            ("</%s>" % self.name)
        )
    
class Document:

    _head = []
    _tail = []
    
    def _tag(self, tagname, *args, **kwargs):
        opentag = "<%s" % tagname
        for x,y in kwargs.iteritems():
            opentag += ' %s="%s"' % ((x[1:] if x[0] == '_' else x), y)
        opentag += ">"
        self._head.append(opentag)
        
        for x in args:
            if type(x) in (list, tuple):
                self._head += list(x)
            elif type(x) in (str, unicode):
                self._head.append(x)
            else:
                x()
                
        self._head.append("</%s>\n" % tagname)
    
    def _text(self, text):
        self._head += [ text ]
        
    def _rewind(self):
        self._tail.append(self._head.pop())
        
    def _forward(self):
        self._head.append(self._tail.pop())
            
    def __getattr__(self, name):
        return DocumentTag(self, name)

    def __repr__(self):
        return "Document Instance"

    
D = Document();

with D.html:
    D.head(D.title("foo"))
    with D.body:
        for y in range(0,3):
            with D.p(_class="bar"):
                for x in range(0,3):
                    D.img(src="baz%d-%d.jpg" % (x,y))
                    D.caption("Testing %d-%d" % (y,x))
            
print ''.join(D._head)