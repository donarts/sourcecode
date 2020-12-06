print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("yield Example1")

def createGenerator():
	yield 2
	yield 3
	yield 1

for i in createGenerator():
	print(i)


print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("yield Example2")

def createGenerator2():
	print("createGenerator2 2")
	yield 2
	print("createGenerator2 3")
	yield 3
	print("createGenerator2 1")
	yield 1

for i in createGenerator2():
	print(i)

"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
yield Example1
2
3
1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
yield Example2
createGenerator2 2
2
createGenerator2 3
3
createGenerator2 1
1
"""