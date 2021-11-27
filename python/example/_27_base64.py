import base64
mytext = "한글입니다.abc"

# bytes로 변환해줍니다.
bytedata = mytext.encode('utf-8')
print("bytedate:",bytedata)

# base64 인코딩을 합니다.
encoded= (base64.b64encode(bytedata))
print("base64encoded:",encoded)

# byte를 text형태로 출력하기 위해서 디코딩을 함
encoded_ascii=encoded.decode('ascii')
print("base64txt:",encoded_ascii)

# decode
text = '7ZWc6riA7J6F64uI64ukLmFiYw=='
strtext = base64.b64decode(text).decode('utf-8')
print(strtext,type(strtext))
strtext = base64.b64decode(text).decode('ascii') # ERROR
print(strtext,type(strtext))
