from os.path import exists
import uiautomator2 as u2
import adbutils
import time
from PIL import Image
from PIL import ImageChops
import math, operator

test_image_name = "testimage.png"
test_package = "com.android.settings"


def write_file(filename,str_data):
	with open(filename, 'w', encoding="utf-8") as fp:
		fp.write(str_data)
		fp.close()
		
def images_are_similar(img1, img2, error=90):
	print(img1.size[0],img1.size[1]) # xsize, ysize
	diff = ImageChops.difference(img1, img2).histogram()
	# [ r 256 , g 256 , b 256 ] = 768 list
	print(len(diff))
	print(diff)
	sq = (value * (i % 256) ** 2 for i, value in enumerate(diff))
	sum_squares = sum(sq)
	print(sum_squares)
	rms = math.sqrt(sum_squares / float(img1.size[0] * img1.size[1]))
	print(rms)
	return rms < error
	
if __name__ == "__main__":
	d = None
	for dev in adbutils.adb.device_list():
		print("Dev:", dev)
		d = u2.connect(dev.serial)

	if d==None:
		print("please check connected devices (adb devices)")
	else:
		d.screen_on()
		d.unlock()
		d.press("home")

		print(d.app_current())
		d.app_start(test_package)
		pid = d.app_wait(test_package, timeout=20.0)
		if not pid:
			print(f"{test_package} is not running")
		else:
			print(f"{test_package} pid is {pid}")

		xml = d.dump_hierarchy()
		print("saving xml")
		write_file("hierarchy.xml",str(xml))
		image = d.screenshot()
		if not exists(test_image_name):
			image.save(test_image_name)
			print("save screenshot")
		else:
			# compare
			image.save("new"+test_image_name)
			pimage = Image.open(test_image_name)
			#for test sdiff = images_are_similar(image,image)
			sdiff = images_are_similar(image,pimage)
			print(sdiff)
		print(d.app_current())
		d.press("home")

