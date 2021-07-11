global val1

val1 = 10
val2 = [10,20,30]

# py scriptiong
print("Script main")
print('main val1',val1)
print('main val2',val2)
data = exec(open('10_py_scripting_script.py').read())
print('return',data)
print('main val1',val1)
print('main val2',val2)

'''
Script main
main val1 10
main val2 [10, 20, 30]
in script
__name__ __main__
main val1 10
main val2 [10, 20, 30]
return None
main val1 100
main val2 [10, 200, 30]
'''
