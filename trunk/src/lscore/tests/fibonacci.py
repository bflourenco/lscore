def fib(n):
	i = 0
	a,b = 0,1
	while i < n:
		a,b = b,a+b
		i += 1
	return b
axiom = 'A(4)'
rules:
A(t):1:1:A(fib(t)):
