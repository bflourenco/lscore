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