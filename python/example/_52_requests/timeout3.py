import requests
import datetime
import traceback
import time
import socket

def url_connect(url, timeout=None):
    nowtime = datetime.datetime.now()
    try:
        print(f"********** trying connect {url} *************")
        if timeout != None:
            r = requests.get(url, timeout=timeout)
        else:
            r = requests.get(url)
        print(r)
    except Exception as e:
        print("end time:", datetime.datetime.now() - nowtime)
        time.sleep(1)
        print("EXCEPTION", e)
        traceback.print_exc()


if __name__ == "__main__":
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   s.connect(("8.8.8.8", 80))
   myip = s.getsockname()[0]
   print(myip)
   s.close()
   url_connect(f"http://{myip}:8080", timeout=1)
