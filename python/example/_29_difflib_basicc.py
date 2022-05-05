import difflib
import sys
from pprint import pprint
text1 = "  1. Beautiful is \n  2. better \n  3. than ugly. \n  4. Explicit is better than implicit.\n  5. Simple is better than complex.\n  6. Complex is better than complicated.\n"
text2 = "  1. Beautiful is \n  2. better \n  3. than ugly. \n  4. Explicit is better than implicit.\n  5. Simple is betr than complex.\n  6. Comaaaplex is better than compddlicated.\n"
text1 = text1.splitlines()
text2 = text2.splitlines()
d = difflib.Differ()
result = list(d.compare(text1, text2))
print("\n".join(result)) # 모든 리스트를 합칩니다.리스트를 합칠때 개행을 입력합니다.
'''
    1. Beautiful is
    2. better
    3. than ugly.
    4. Explicit is better than implicit.
-   5. Simple is better than complex.
?                   --

+   5. Simple is betr than complex.
-   6. Complex is better than complicated.
+   6. Comaaaplex is better than compddlicated.
?         +++                        ++
'''


print("ndiff")
'''a와 b(문자열의 리스트)를 비교합니다; Differ-스타일 델타(델타 줄을 생성하는 제너레이터)를 반환합니다.'''
result = list(difflib.ndiff(text1, text2))
print("\n".join(result)) 
'''
ndiff
    1. Beautiful is
    2. better
    3. than ugly.
    4. Explicit is better than implicit.
-   5. Simple is better than complex.
?                   --

+   5. Simple is betr than complex.
-   6. Complex is better than complicated.
+   6. Comaaaplex is better than compddlicated.
?         +++                        ++
'''


print("unified_diff")
'''
a와 b(문자열의 리스트)를 비교합니다; 델타(델타 줄을 생성하는 제너레이터)를 통합 diff 형식으로 반환합니다.
통합(unified) diff는 단지 변경된 줄과 몇 줄의 문맥만을 더해서 표시하는 간결한 방법입니다. 
변경 사항은 (별도의 이전/이후 블록 대신) 인라인 스타일로 표시됩니다. 문맥 줄의 수는 n에 의해 설정되며 기본값은 3입니다.
'''
result = list(difflib.unified_diff(text1, text2))
print("\n".join(result)) 
'''
unified_diff
---

+++

@@ -2,5 +2,5 @@

   2. better
   3. than ugly.
   4. Explicit is better than implicit.
-  5. Simple is better than complex.
-  6. Complex is better than complicated.
+  5. Simple is betr than complex.
+  6. Comaaaplex is better than compddlicated.
'''



print("context_diff")
result = list(difflib.context_diff(text1, text2))
print("\n".join(result)) 
'''
context_diff
***

---

***************

*** 2,6 ****

    2. better
    3. than ugly.
    4. Explicit is better than implicit.
!   5. Simple is better than complex.
!   6. Complex is better than complicated.
--- 2,6 ----

    2. better
    3. than ugly.
    4. Explicit is better than implicit.
!   5. Simple is betr than complex.
!   6. Comaaaplex is better than compddlicated.
'''

print("HtmlDiff")
result = list(difflib.HtmlDiff().make_file(text1, text2))
print("".join(result)) 
'''
HtmlDiff

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html>

<head>
    <meta http-equiv="Content-Type"
          content="text/html; charset=utf-8" />
    <title></title>
    <style type="text/css">
        table.diff {font-family:Courier; border:medium;}
        .diff_header {background-color:#e0e0e0}
        td.diff_header {text-align:right}
        .diff_next {background-color:#c0c0c0}
        .diff_add {background-color:#aaffaa}
        .diff_chg {background-color:#ffff77}
        .diff_sub {background-color:#ffaaaa}
    </style>
</head>

<body>

    <table class="diff" id="difflib_chg_to0__top"
           cellspacing="0" cellpadding="0" rules="groups" >
        <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup>
        <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup>

        <tbody>
            <tr><td class="diff_next" id="difflib_chg_to0__0"><a href="#difflib_chg_to0__0">f</a></td><td class="diff_header" id="from0_1">1</td><td nowrap="nowrap">&nbsp;&nbsp;1.&nbsp;Beautiful&nbsp;is&nbsp;</td><td class="diff_next"><a href="#difflib_chg_to0__0">f</a></td><td class="diff_header" id="to0_1">1</td><td nowrap="nowrap">&nbsp;&nbsp;1.&nbsp;Beautiful&nbsp;is&nbsp;</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_2">2</td><td nowrap="nowrap">&nbsp;&nbsp;2.&nbsp;better&nbsp;</td><td class="diff_next"></td><td class="diff_header" id="to0_2">2</td><td nowrap="nowrap">&nbsp;&nbsp;2.&nbsp;better&nbsp;</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_3">3</td><td nowrap="nowrap">&nbsp;&nbsp;3.&nbsp;than&nbsp;ugly.&nbsp;</td><td class="diff_next"></td><td class="diff_header" id="to0_3">3</td><td nowrap="nowrap">&nbsp;&nbsp;3.&nbsp;than&nbsp;ugly.&nbsp;</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_4">4</td><td nowrap="nowrap">&nbsp;&nbsp;4.&nbsp;Explicit&nbsp;is&nbsp;better&nbsp;than&nbsp;implicit.</td><td class="diff_next"></td><td class="diff_header" id="to0_4">4</td><td nowrap="nowrap">&nbsp;&nbsp;4.&nbsp;Explicit&nbsp;is&nbsp;better&nbsp;than&nbsp;implicit.</td></tr>
            <tr><td class="diff_next"><a href="#difflib_chg_to0__top">t</a></td><td class="diff_header" id="from0_5">5</td><td nowrap="nowrap">&nbsp;&nbsp;5.&nbsp;Simple&nbsp;is&nbsp;bet<span class="diff_sub">te</span>r&nbsp;than&nbsp;complex.</td><td class="diff_next"><a href="#difflib_chg_to0__top">t</a></td><td class="diff_header" id="to0_5">5</td><td nowrap="nowrap">&nbsp;&nbsp;5.&nbsp;Simple&nbsp;is&nbsp;betr&nbsp;than&nbsp;complex.</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_6">6</td><td nowrap="nowrap">&nbsp;&nbsp;6.&nbsp;Complex&nbsp;is&nbsp;better&nbsp;than&nbsp;complicated.</td><td class="diff_next"></td><td class="diff_header" id="to0_6">6</td><td nowrap="nowrap">&nbsp;&nbsp;6.&nbsp;Com<span class="diff_add">aaa</span>plex&nbsp;is&nbsp;better&nbsp;than&nbsp;comp<span class="diff_add">dd</span>licated.</td></tr>
        </tbody>
    </table>
    <table class="diff" summary="Legends">
        <tr> <th colspan="2"> Legends </th> </tr>
        <tr> <td> <table border="" summary="Colors">
                      <tr><th> Colors </th> </tr>
                      <tr><td class="diff_add">&nbsp;Added&nbsp;</td></tr>
                      <tr><td class="diff_chg">Changed</td> </tr>
                      <tr><td class="diff_sub">Deleted</td> </tr>
                  </table></td>
             <td> <table border="" summary="Links">
                      <tr><th colspan="2"> Links </th> </tr>
                      <tr><td>(f)irst change</td> </tr>
                      <tr><td>(n)ext change</td> </tr>
                      <tr><td>(t)op</td> </tr>
                  </table></td> </tr>
    </table>
</body>

</html>
'''