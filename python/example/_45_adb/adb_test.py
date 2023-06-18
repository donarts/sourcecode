from adbutils import adb

d = adb.device()    


ret = d.sync.push("aapt", "/data/local/tmp/aapt") 
ret = d.shell2("chmod 777 /data/local/tmp/aapt")
print(ret.output)
ret = d.shell2("ls -l /data/local/tmp/aapt")
print(ret.output)

ret = d.shell2("pm list packages -f")
linelist = ret.output.split("\n")

for oneline in linelist:
    if "=" in oneline:
        pkgname = oneline[oneline.rindex("=")+1:]
        apkpath = oneline[:oneline.rindex("=")]
        apkpath = apkpath[8:]
        #print(apkpath)
        
        ret = d.shell2("ls -l /data/local/tmp/aapt")
        print(ret.output)
        ret = d.shell2(f"/data/local/tmp/aapt dump badging {apkpath}")
        print(ret.output)
        
        #info = d.package_info(f"{pkgname}")
        #if info:
        #    print(info) 
        
        ret = d.shell2(f"ls -l {apkpath}")
        size = ret.output.split(" ")[4]
        if apkpath.startswith("/system/"):
            path = "system"
        elif apkpath.startswith("/product/"):
            path = "product"
        elif apkpath.startswith("/vendor/"):
            path = "vendor"
        elif apkpath.startswith("/data/"):
            path = "data"
        elif apkpath.startswith("/apex/"):
            path = "apex"
        else:
            path = apkpath
        print(f"{pkgname} , {size} , {path}")

        #ret = d.shell2(f"dumpsys package {pkgname}")
        #print(ret.output)
        break

#ret = d.shell2(f"dumpsys activity")
#print(ret.output)      

#ret = d.shell2(f'dumpsys window windows')
#print(ret.output)      


 