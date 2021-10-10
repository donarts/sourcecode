
def f0(x):
	return x[0]

def f1(x):
	return x[1]
	
def f2(x):
	return x[1][2]

if __name__ == "__main__":
	dict_test = {'ccc':300,'aaa':100,'bbb':200, 'ddd':150}
	
	print("\n key sort")
	rdata = sorted(dict_test)
	print(rdata)
	for x in rdata:
		print(x,dict_test[x])
		
	print("\n key sort reverse")
	rdata = sorted(dict_test,reverse=True)
	print(rdata)
	for x in rdata:
		print(x,dict_test[x])
	
	print("\n value sort")
	rdata = sorted(dict_test.items(),key=f1)
	print(rdata)
	for x,y in rdata:
		print(x,y)
		
	print("\n value sort reverse")
	rdata = sorted(dict_test.items(),key=f1,reverse=True)
	print(rdata)
	for x,y in rdata:
		print(x,y)

	print("\n key sort")
	rdata = sorted(dict_test.items(),key=f0)
	print(rdata)
	for x,y in rdata:
		print(x,y)
	
	dict_test = {'ccc':[100,300,140],'aaa':[200,400,300],'bbb':[100,40,300], 'ddd':[100,20,30]}
	print("\n list value sort")
	rdata = sorted(dict_test.items(),key=f2)
	print(rdata)
	for x,y in rdata:
		print(x,y)
	
	'''
	x[1][2]
	-------
	x[0]:'ccc'
	x[1]:[100,300,140] 
	x[1][0]:100
	x[1][1]:300
	x[1][2]:140
	'''
