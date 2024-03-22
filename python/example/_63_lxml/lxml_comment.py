from lxml import etree

xml_str = \
"""<?xml version="1.0" encoding="UTF-8"?>
<!-- hello -->
<note>
  <!-- dash1 -->
  <to>kim</to><!-- dash2 -->
  <from>lee</from>
  <heading>alert</heading>
  <body>i am a boy</body>
</note>
"""

def print_xml(xml_str_):
    # XML 파일을 불러옵니다.
    root = etree.fromstring(xml_str.encode())

    # 루트 엘리먼트의 태그와 속성을 출력합니다.
    print(f'Root element: {root.tag}')
    for name, value in root.attrib.items():
        print(f'Attribute - {name}: {value}')

    # 모든 자식 엘리먼트를 순회하며 출력합니다.
    for child in root:
        print(f'Child element: {child.tag}')
        for name, value in child.attrib.items():
            print(f'Attribute - {name}: {value}')

def print_xml_wc(xml_str_):
    # XML 파일을 불러옵니다.
    root = etree.fromstring(xml_str.encode())

    # 루트 엘리먼트의 태그와 속성을 출력합니다.
    print(f'Root element: {root.tag}')
    for name, value in root.attrib.items():
        print(f'Attribute - {name}: {value}')

    # 모든 자식 엘리먼트를 순회하며 출력합니다.
    for child in root:
        print(f'Child element: {child.tag}')
        if child.tag == etree.Comment:
            print("comment:", child.text)
            continue
        for name, value in child.attrib.items():
            print(f'Attribute - {name}: {value}')


def print_xml_wc_root(xml_str_):
    # XML 파일을 불러옵니다.
    root = etree.fromstring(xml_str.encode())

    if root.getprevious() != None:
        if root.getprevious().tag == etree.Comment:
            print("comment:", root.getprevious().text)

    # 루트 엘리먼트의 태그와 속성을 출력합니다.
    print(f'Root element: {root.tag}')
    for name, value in root.attrib.items():
        print(f'Attribute - {name}: {value}')

    # 모든 자식 엘리먼트를 순회하며 출력합니다.
    for child in root:
        print(f'Child element: {child.tag}')
        if child.tag == etree.Comment:
            print("comment:", child.text)
            continue
        for name, value in child.attrib.items():
            print(f'Attribute - {name}: {value}')

print("1")
print_xml(xml_str)
print("2")
print_xml_wc(xml_str)
print("3")
print_xml_wc_root(xml_str)

