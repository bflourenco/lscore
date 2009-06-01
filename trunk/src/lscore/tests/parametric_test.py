axiom = 'B(2)A(4,4)'
rules:
A(x,y): y <= 3 : 1 : A(x*2,x+y):
A(x,y): y  > 3 : 1 : B(x)A(x/y,0):
B(x)  : x < 1  : 1 : C:
B(x)  : x >= 1 : 1 : B(x-1):
