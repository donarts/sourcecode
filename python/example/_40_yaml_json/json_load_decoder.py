import json
code = "" \
       '''
       {
       "a":"안녕하세요\n반갑습니다."
       }
       '''
print(code)

# json.decoder.JSONDecodeError: Invalid control character at: line 3 column 18 (char 27)
# https://docs.python.org/ko/3/library/json.html#json.JSONDecoder
# strict가 거짓이면 (True가 기본값입니다), 문자열 안에 제어 문자가 허용됩니다. 이 문맥에서 제어 문자는 0–31 범위의 문자 코드를 가진 것들인데, '\t' (탭), '\n', '\r' 및 '\0'을 포함합니다.

json_data = json.loads(code, strict=False)
print(json_data)

