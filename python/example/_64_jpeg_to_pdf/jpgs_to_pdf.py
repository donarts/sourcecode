import os
from PIL import Image
import natsort
from collections import Counter

#특정 폴더의 jpg 파일들을 모두 하나의 pdf 파일로 묶습니다.
#이때 가로 크기를 모두 같은 크기로 변경합니다.

def jpgs_to_pdf(folder_path, output_pdf_path):
    # 지정된 폴더에서 JPG 파일 리스트 가져오기
    jpg_files = [f for f in natsort.natsorted(os.listdir(folder_path)) if f.lower().endswith('.jpg')]
    print(jpg_files)
    if not jpg_files:
        print("폴더에 JPG 파일이 없습니다.")
        return

    # 모든 이미지의 가로 크기 확인
    widths = []
    for jpg_file in jpg_files:
        img_path = os.path.join(folder_path, jpg_file)
        with Image.open(img_path) as img:
            widths.append(img.width)

    counter = Counter(widths)
    most_common_value, most_common_count = counter.most_common(1)[0]

    # 가장 작은 가로 크기 찾기
    smallest_width = min(widths)
    print(f"가장 작은 가로 크기: {smallest_width} mean:{sum(widths)/len(widths)} 전체갯수:{len(widths)} 많은값:{most_common_value} 많은갯수:{most_common_count}")

    smallest_width = most_common_value

    # 이미지 리스트 생성
    images = []
    for jpg_file in jpg_files:
        img_path = os.path.join(folder_path, jpg_file)
        img = Image.open(img_path)

        if smallest_width != img.width:
            # 비율에 맞춰 리사이즈
            aspect_ratio = img.height / img.width
            new_height = int(smallest_width * aspect_ratio)
            resized_img = img.resize((smallest_width, new_height), Image.LANCZOS)
            images.append(resized_img.convert('RGB'))  # RGB로 변환
        else:
            images.append(img.convert('RGB'))  # RGB로 변환

    if images:
        # 첫 번째 이미지를 기반으로 PDF 생성
        first_image = images.pop(0)
        first_image.save(output_pdf_path, save_all=True, append_images=images)

# 사용 예시
folder_path = r"D:/temp/output"
output_pdf_path = 'D:/temp/output.pdf'  # 생성될 PDF 파일 경로
jpgs_to_pdf(folder_path, output_pdf_path)

print(f"{output_pdf_path} 파일이 생성되었습니다.")