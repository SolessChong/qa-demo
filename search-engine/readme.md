## Problems
### Parsing large XML files
The input xml file is 4GB, plain xml.etree.parse() freezes at parsing.
So we have to use iterative parsing to make it linear as well as stop at proper time.
We followed the this [blog post](http://boscoh.com/programming/reading-xml-serially.html) to solve it.

