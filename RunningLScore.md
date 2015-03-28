# Dependencies #
**python**pygtk and pygtksourceview2 - (for the GTK interface)

# Downloading the Files #
Download the files from the subversion repository:

svn checkout http://lscore.googlecode.com/svn/trunk/ lscore

# Details #
To run the program:

python lscoremain.py (for the gtk interface)

python lscorecli.py (for the command line)

# The rules file #

<python code>
axiom = "something"
rules:
predecessor:condition:probability:sucessor
.
.
.

Examples:
The Hilbert Curve:
```
axiom = '-X'
rules:
X:1:1:-YF+XFX+FY-
Y:1:1:+XF-YFY-FX+
```
Context-Sensitive(abop, page 35-b):

```
axiom = "F1F1F1"
ignore = set(['+','-','F'])
rules:
0<0>0:1:1:0
0<0>1:1:1:1[-F1F1]
0<1>0:1:1:1
0<1>1:1:1:1
1<0>0:1:1:0
1<0>1:1:1:1F1
1<1>0:1:1:1
1<1>1:1:1:0
+:1:1:-
-:1:1:+
```
Parametric:
```
axiom = 'B(2)A(4,4)'
rules:
A(x,y): y <= 3 : 1 : A(x*2,x+y)
A(x,y): y  > 3 : 1 : B(x)A(x/y,0)
B(x)  : x < 1  : 1 : C
B(x)  : x >= 1 : 1 : B(x-1)
```

Before the 'rules:' statement you can put some python code if you want,
for example you can write a small function and then call it inside a
rule. Example:
```
def fib(n):
	i = 0
	a,b = 0,1
	while i < n:
		a,b = b,a+b
		i += 1
	return b
axiom = 'A(4)'
rules:
A(t):1:1:A(fib(t))
```
The result will be A(4), A(5), A(8), A(34)...