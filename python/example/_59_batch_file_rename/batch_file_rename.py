import os

# 주어진 디렉토리에 있는 항목들의 이름을 담고 있는 리스트를 반환합니다.
# 리스트는 임의의 순서대로 나열됩니다.
file_path = r'C:\Users\jun\Downloads\download (1)\even'
page = 2
file_names = os.listdir(file_path)
print(file_names)
# ['00001.jpg', '00002.jpg' ...
for name in file_names:
    print(os.path.splitext(name))
    # ('00001', '.jpg')
    # ('00002', '.jpg')
    # ...
    file_name = os.path.splitext(name)[0]
    ext_name = os.path.splitext(name)[1]

    src = os.path.join(file_path, name)
    dst = 'B' + str(page).zfill(5) + '.jpg'
    dst = os.path.join(file_path, dst)
    os.rename(src, dst)
    print(f'{src} -> {dst}')
    page += 2
