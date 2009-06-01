axiom = "O(0)O(6)O(5)O(2)O(10)"
rules:
O(e)<O(n)>O(d): (n >= e) and (n <= d) : 1 :  O(n):
O(e)<O(n)>O(d): (n >= e) and (n > d) : 1 :  O(d)O(n):
O(e)<O(n)>O(d): (n < e) and (n <= d) : 1 :: 
O(e)<O(n)>O(d): (n < e) and (n > d) : 1 :  O(d):

