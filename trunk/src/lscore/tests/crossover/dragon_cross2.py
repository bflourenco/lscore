axiom = "FXA(0)"
rules:
X:1:1:X+YF+:
Y:1:1:-FX-Y:
A(t):(t != 6):1:A(t+1):
A(t):(t==6):1:A(t+1):crossover(0,1)