axiom = '-XA(0)B(0)'
#seed = 6
seed = 10
rules:
X:1:1:-YF+XFX+FY-:
Y:1:1:+XF-YFY-FX+:
A(t): (t % 2)==0 :1:A(t+1):crossover(0,1)
A(t): (t % 2)!=0:1:A(t+1):
B(t): t==3 :1:B(t+1):mutation(0)
B(t): t !=3:1:B(t+1):