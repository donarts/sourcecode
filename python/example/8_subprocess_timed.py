import subprocess
import psutil
import os
import threading

class TimeoutThread(threading.Thread):
	def __init__(self, pid, timeout, event):
		threading.Thread.__init__(self)
		self.pid = pid
		self.timeout = timeout
		self.event = event
		self.setDaemon(True)
		self.istimeout = False

	def kill(self,proc_pid):
		process = psutil.Process(proc_pid)
		for proc in process.children(recursive=True):
			proc.kill()
		process.kill()
	
	def run(self):
		self.event.wait(self.timeout)
		if not self.event.isSet():
			self.istimeout = True
			try:
				self.kill(self.pid)
			except Exception as e:
				print(e)
				pass

def subprocess_timed(path_cmd, timeout, pipe=True):
	event = threading.Event()
	abspath = os.path.abspath(path_cmd)
	head, tail = os.path.split(abspath)
	if pipe==True:
		proc = subprocess.Popen(tail, cwd = head, shell=False, stdout=subprocess.PIPE)
	else:
		proc = subprocess.Popen(tail, cwd = head, shell=False)
	tothread = TimeoutThread(proc.pid, timeout, event)
	tothread.start()
	
	# waiting for finishing subprocess
	(outs, errs) = proc.communicate()
	event.set()
	
	return (tothread.istimeout,proc.returncode, outs, errs)
	
if __name__ == "__main__":
	print("** Test1 **")
	print(subprocess_timed("python 8_exit_code.py",6))
	print("** Test2 **")
	print(subprocess_timed("python 8_exit_code_with_sleep.py",6))
	print("** Test3 **")
	print(subprocess_timed("python 8_exit_code_with_sleep.py",4))
	print("** Test4 **")
	print(subprocess_timed("python 8_exit_code.py",6,pipe=False))
