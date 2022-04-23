import os
import sys

def check_platform():
	return sys.platform

def get_data():
	import data.data
	return data.data.get_d_data()