import subprocess

# call is blocking:
subprocess.call('notepad.exe')
print("subprocess.call('notepad.exe')") # executed when notepad is closed

# run is blocking:
subprocess.run('notepad.exe')
print("subprocess.run('notepad.exe')") # executed when notepad is closed

# Popen is non-blocking:
subprocess.Popen('notepad.exe')
print("subprocess.Popen('notepad.exe')") # immediately executed
