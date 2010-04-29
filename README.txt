==================
 NonTemplate v0.1
==================

For more information, see <http://code.zoic.org/nontemplate/>.

Summary
=======

* NonTemplate allows you to generate simple XML output directly
  in your Python code with a minimum of syntactic noise.

* It uses the **with** statement introduced in Python 2.5 to ensure
  that once a tag is opened, it will be closed.

* Python code and template codes can be interleaved naturally,
  without resorting to restrictive language constructions.
  Your favourite debugger can see, and set breakpoints in, every
  level of your template.

* 100% pure Python (>= 2.5), and it works just fine in Python
  3.0 as well.
   
* Performance is comparable to the commonly used templating languages
  and is better than most.

* Asyncronous use is easy: NonTemplate is happy reading from iterables
  and writing to IO streams.  This means you can start sending XHTML
  to your clients while your database is still retrieving rows ... 


Example
=======
::

 import nontemplate

 D = nontemplate.document
 with D.html():
   D._comment("this is a test")
   with D.head():
     D.title("foo")
   with D.body():
     with D.h1(id="foo"):
       D._text("This is a test")
     with D.table(_class="cool"):
       with D.tbody():
	 for row in range(1,11):
	   with D.tr():
	     for col in range(1,11):
	       if row == col:
	         D.td(_class="same")("%d" % row)
	       else:
	         D.td(_class="diff")("%d,%d" % (row,col))

