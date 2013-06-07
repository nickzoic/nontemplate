===================
 NonTemplate v0.12
===================

For more information, see <http://code.zoic.org/nontemplate/>.

Summary
=======

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
=======
::

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

