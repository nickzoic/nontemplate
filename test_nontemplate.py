#!/usr/bin/env python

from __future__ import with_statement

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


expected = """<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<html>
<!-- this is a test -->
<!-- this --&gt; is too -->
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

if str(D) == expected:
    print("YAY")
else:
    print("FAIL")
    print(str(D))
    exit(1)	
