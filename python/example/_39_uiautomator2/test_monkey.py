from adbutils import adb
import re

class adb_utils_rp():
	def adb_connect(self, serial=None):
		self.d = adb.device(serial=serial)
		if self.d.serial==None :
			return None
		print("adb conneced",self.d.serial)
		return self.d

	def get_prop(self, keyname=None):
		ret_dict = {}
		# 전체 poperty 는 getprop 명령으로 획득 가능합니다.
		ret = self.d.shell("getprop")
		#print(ret)
		retlines = ret.replace("]\n","]\0")
		retlines = retlines.split("\0")
		
		for one_line in retlines:
			one_line = one_line.replace("]: [","]"+"\0"+"[")
			dat = one_line.split("\0")
			#print(dat)
			dat1 = dat[1].strip()
			ret_dict[dat[0][1:len(dat[0])-1]] = dat1[1:len(dat1)-1]
			#print(dat[0][1:len(dat[0])-1],ret_dict[dat[0][1:len(dat[0])-1]])
		
		if keyname==None:
			return ret_dict
		
		return ret_dict.get(keyname)

	def make_bugreportz(self, log_zip_filename="log.zip"):
		# bugreportz 는 /data/user_de/0/com.android.shell/files/bugreports/ 에 로그를 생성하며 생성시 이전로그가 삭제 됩니다.
		#            리턴값은 OK:로 시작하며 뒤에는 경로명이 넘어 옵니다.
		#            예) OK:/data/user_de/0/com.android.shell/files/bugreports/dumpstate-2022-05-14-17-33-03.zip
		#
		# 동작중 다시 호출하면 아래와 같은 string이 리턴됩니다.
		# Previous sys dump or full dump is running, so skip this one

		ret = self.d.shell("bugreportz")
		print(ret)

		isok = ret.split(":")
		if len(isok)!=2 or isok[0]!='OK':
			return -1
		
		# 로그 뜬뒤 로그 버퍼를 초기화한다.
		self.d.shell("logcat -b all -c")
		
		# return 은 int size가 넘어옵니다.
		# 파일이 없으면 exception 발생합니다.
		#    adbutils.errors.AdbError: open failed: No such file or directory
		ret=self.d.sync.pull(isok[1], log_zip_filename)
		if ret==0:
			return -2
		
		# int size 가 리턴됩니다.
		return ret
		
	#EVENT LOG (logcat -b events -v threadtime -v printable -v uid -d *:v)
	def get_event_log(self):
		ret = self.d.shell("logcat -b events -v threadtime -v printable -v uid -d *:v")
		#print(ret)
		return ret
		
	# @return
	# None : 오류 없음
	# else : 오류 있음
	def check_event_log(self):
		find_str = "(am_crash)|(am_anr)"
		ret = self.get_event_log()
		#ret = " \n\n\n\n am_cras \n  am_anr "
		finded = re.search(find_str,ret)
		return finded
		
	def monkey(self,package,count,seed=0,throttle=300,extra=""):
		return self.d.shell(f"monkey -p {package} -s {seed} --throttle {throttle} {extra} -v {count}")
		
if __name__ == "__main__":
	adbrp = adb_utils_rp()
	adbrp.adb_connect()
	print(adbrp.get_prop("ro.serialno"))
	print(adbrp.get_prop("ro.build.fingerprint"))
	#print(adbrp.make_bugreportz())
	
	# test가 종료될때까지 기다리게 됩니다.
	print(adbrp.monkey("com.android.chrome",500))
	
	#print(adbrp.get_event_log())
	#print(adbrp.check_event_log())
	if adbrp.check_event_log()!=None:
		adbrp.make_bugreportz()
