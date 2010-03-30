#!/usr/bin/env python

class Element:
    
    def __init__(self, document, name):
        self.document = document
        self.parent = document._cursor
        self.children = []
        self.name = name
        self.attrs = []
        print "INIT %s" % self.name
        
    def __enter__(self):
        print "ENTER %s" % self.name
        self.document._cursor = self
    
    def __exit__(self, *stuff):
        print "EXIT %s" % self.name
        self.document._cursor = self.parent

    def __call__(self, *args, **kwargs):
        print "CALL %s" % self.name
        self.attrs += [ (k[1:] if k[0] == '_' else k, v) for k, v in kwargs.iteritems() ]
        self.children += args
        return self
        
    def append(self, elem):
        self.children.append(elem)

    def __str__(self):
        xml =  ("<%s" % self.name) + (''.join( ' %s="%s"' % (k, v) for k, v in self.attrs))
        if self.children:
            xml += ">" + (''.join( [str(e) for e in self.children] )) + ("</%s>\n" % self.name)
        else:
            xml += "/>\n";
        return xml
    
class Document:

    _cursor = []
    
    def __getattr__(self, name):
        '''calling D.foo() causes this to be run ...'''
        newelem = Element(self, name)
        self._cursor.append(newelem)
        return newelem
    
    def __str__(self):
        return "\n".join(str(e) for e in self._cursor)

#----------------------------------------------------------------------------

D = Document();

with D.html:
    D.head(D.title("foo"), D.meta("something"))
    D.neck("ha ha ha")
    with D.body:
        for y in range(0,3):
            with D.p(_class = "bar"):
                for x in range(0,3):
                    D.img(src="baz%d-%d.jpg" % (x,y))
                    D.caption("Testing %d-%d" % (y,x))
            
print str(D)