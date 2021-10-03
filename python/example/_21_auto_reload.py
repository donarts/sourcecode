import time
import os
import subprocess
import sys

import _19_check_file_mod

def get_args_for_reloading():
	py_exe = [sys.executable]
	py_script = sys.argv[0]
	args = sys.argv[1:]
	print(py_exe,py_script,args)
	
	ret=[]
	ret.extend(py_exe)
	ret.append(py_script)
	ret.extend(args)
	return ret

def reload():
	print("reload")
	args = get_args_for_reloading()
	new_environ = os.environ.copy()
	if os.environ.get("RE_LOAD")=="true":
		sys.exit(0)
		print("never")
	else:
		while True:
			sys.stdout.flush()
			new_environ["RE_LOAD"] = "true"
			exit_code = subprocess.call(args, env=new_environ)
			print("exit_code:",exit_code)
			time.sleep(1)
			
	print("never")

if __name__ == '__main__':
	check_file_mod = _19_check_file_mod.check_file_mod(sys.argv[0])
	print("start !")
	if os.environ.get("RE_LOAD")=="true":
		print("reloaded")
		
	while True:
		if check_file_mod.is_change():
			print("change")
			reload()
		time.sleep(2)

