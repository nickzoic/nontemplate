nontemplate
===========

> Not Another Templating System for Python

Summary
-------

* NonTemplate allows you to generate simple XML output directly
  in your Python code with a minimum of syntactic noise.

* It uses the **with** statement introduced in Python 2.6 to ensure
  that once a tag is opened, it will be closed.

* Python code and template codes can be interleaved naturally,
  without resorting to restrictive language constructions.
  Your favourite debugger can see, and set breakpoints in, every
  level of your template.

* 100% pure Python (>= 2.6), and it works just fine in Python
  3.0 as well.
   
* Performance is comparable to the commonly used templating languages
  and is better than most.

* Asynchronous use is easy: NonTemplate is happy reading from iterables
  and writing to IO streams.  This means you can start sending XHTML
  to your clients while your database is still retrieving rows ... 


Example
-------

    import nontemplate

    D = nontemplate.Document(doctype=nontemplate.doctype.html_2_0)
    
    with D.html():
        D._comment("this is a test")
        D._comment("this --> is too")
        D._emit("<!-- testing & < > emit -->\n")
        with D.head():
            D.title()("foo")
        with D.body():
            with D.h1(id="foo"):
                D._text("This is a <foo> & test")
            with D.table(_class="cool"):
                with D.tbody():
                    for row in range(1,3):
                        with D.tr():
                            for col in range(1,3):
                                D.td()("%d,%d" % (row,col))


Python 2.5
----------

Nontemplate works fine in Python 2.5 but you have to include

    from __future__ import with_statement
    at the top of whatever module uses it.

License
-------

NonTemplate is Copyright (C) 2010 Nick Moore. It is released under the MIT license. See LICENSE.txt in the source distribution.

History
-------

I first used CGI.pm back in the dawn of Internet time (eg: 1999) and I was impressed by the concept of embedding HTML code directly in Perl, if not the implementation. In Python, lxml.etree's E-factory performs a similar job, but greatly restricts your flexibility with branching and looping constructs.

In the meantime, I've wrestled with all sorts of templating languages in both Perl and Python, none of which have proved to be entirely pleasant to deal with. They each provide a DSL of sorts, offering more or less complexity at more or less of a distance from the 'parent' language.

One aim of template languages has always been to separate "coding" from "web design", so that a web designer is not exposed to the full horror of actual code. The parts of the template code which intrude upon the HTML are generally marked up with strange punctuation and the web designed could be warned not to touch those parts ... sometimes this even worked! However, in modern practice, Cascading Stylesheets provide a separation of content from presentation, rendering this point moot.

One big inspiration for this project has been wrestling with the really quite daft Django template engine. Just for posterity, my least disliked Python template language is Mako, mostly because it is the fastest of the bunch, and it doesn't reinvent many wheels.

In a better world, this work would be in vain, because the only HTML you'd have to write would be a wrapper to bootstrap a suitable AJAX system and everything would be XML or JSON from there. However, I still find myself using template languages with regrettable regularity.


Download & Install
------------------

* The code is all [on github now](https://github.com/nickzoic/nontemplate) 
* Or install [from PyPI](https://pypi.python.org/pypi/nontemplate/0.12)
