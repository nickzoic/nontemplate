#!/usr/bin/env python

import nontemplate

D = nontemplate.Document()
D._doctype(nontemplate.DOCTYPE_HTML_2_0)
with D.html():
    D._comment("this is a test")
    D._comment("this --> is too")
    D._emit("<!-- testing & < > emit -->\n")
    with D.head():
        D.title("foo")
    with D.body():
        with D.h1(id="foo"):
	    D._text("This is a <foo> & test")
        with D.table(_class="cool"):
            with D.tbody():
                for row in range(1,3):
                    with D.tr():
                        for col in range(1,3):
                            D.td("%d,%d" % (row,col))


expected = """<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<html>
<!-- this is a test -->
<!-- this -- > is too -->
<!-- testing & < > emit -->
<head>
<title>
foo
</title>
</head>
<body>
<h1 id="foo">
This is a &lt;foo&gt; &amp; test
</h1>
<table class="cool">
<tbody>
<tr>
<td>
1,1
</td>
<td>
1,2
</td>
</tr>
<tr>
<td>
2,1
</td>
<td>
2,2
</td>
</tr>
</tbody>
</table>
</body>
</html>
"""

print "YAY" if str(D) == expected else str(D)
