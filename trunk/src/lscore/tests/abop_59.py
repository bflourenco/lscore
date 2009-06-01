level = 10
r1 = 0.9
r2 = 0.7
a1 = 10
a2 = 60
wr = 0.707
axiom = "A(1,10)"
rules:
A(l,w):1:1:!(w)F(l)[&(a1 )B(l*r1 ,w*wr )]/(180)[&(a2 )B(l*r2 ,w*wr )]:
B(l,w):1:1:!(w)F(l)[+(a1)$B(l*r1,w*wr)][-(a2)$B(l*r2,w*wr)]:
