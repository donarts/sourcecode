import mypkg

print(mypkg.check_platform())
print("---")
print(mypkg.get_data())

'''
win32
Traceback (most recent call last):
  File "test.py", line 4, in <module>
    print(mypkg.get_data())
  File "C:/Users/USER/AppData/Local/Programs/Python/Python38/lib/site-packages/mygithub-0.1.0-py3.8.egg/mypkg/__init__.py", line 8, in get_data
    import data.data
  File "C:/Users/USER/Documents/GitHub/sourcecode/python/example/_41_github_install_pkg/data/data.py", line 1
    def get_d_data()
                   ^
SyntaxError: invalid syntax

'''