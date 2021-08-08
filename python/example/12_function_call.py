print("call by value")

a = 100
print(id(a),type(a),a)

b = a
print(id(b),type(b),b)

def fun_a(c):
	print(id(c),type(c),c)
	c = 200
	print(id(c),type(c),c)

fun_a(b)
print(id(b),type(b),b)



print("call by reference")
a = [100]
print(id(a),type(a),a)

b = a
print(id(b),type(b),b)

def fun_a(c):
	print(id(c),type(c),c)
	c = 200
	print(id(c),type(c),c)

def fun_b(c):
	print(id(c),type(c),c)
	c[0] = 200
	print(id(c),type(c),c)

fun_a(b)
print(id(b),type(b),b)
fun_b(b)
print(id(b),type(b),b)

'''
call by value
140714474676992 <class 'int'> 100
140714474676992 <class 'int'> 100
140714474676992 <class 'int'> 100
140714474680192 <class 'int'> 200
140714474676992 <class 'int'> 100
call by reference
2054172649856 <class 'list'> [100]
2054172649856 <class 'list'> [100]
2054172649856 <class 'list'> [100]
140714474680192 <class 'int'> 200
2054172649856 <class 'list'> [100]
2054172649856 <class 'list'> [100]
2054172649856 <class 'list'> [200]
2054172649856 <class 'list'> [200]
'''
