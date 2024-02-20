import requests
import datetime
import traceback
import time


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
    url_connect("http://1.1.1.1:9999")
    url_connect("http://192.168.0.254")
    url_connect("http://127.0.0.1")
    url_connect("http://192.168.0.254", timeout=10)
