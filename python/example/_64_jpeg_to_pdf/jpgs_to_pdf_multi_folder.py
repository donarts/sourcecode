import os
from PIL import Image
import natsort
from collections import Counter

def jpgs_to_pdf(folder_paths, output_pdf_path, jpeg_quality=100, crop_percent=0.0):
    # 지정된 폴더 목록을 순서대로 순회하면서 JPG 파일 리스트 만들기
    image_paths = []
    for folder_path in folder_paths:
        if not os.path.isdir(folder_path):
            print(f"폴더를 찾을 수 없습니다: {folder_path}")
            continue

        # 폴더 내부 파일명 오름차순 정렬
        jpg_files = [
            f for f in natsort.natsorted(os.listdir(folder_path))
            if f.lower().endswith('.jpg')
        ]
        image_paths.extend([os.path.join(folder_path, f) for f in jpg_files])

    print(image_paths)
    if not image_paths:
        print("지정된 폴더들에 JPG 파일이 없습니다.")
        return

    # 모든 이미지의 가로 크기 확인
    widths = []
    for img_path in image_paths:
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
    for img_path in image_paths:
        img = Image.open(img_path)

        # 이미지 크롭
        if crop_percent > 0:
            crop_amount_w = int(img.width * crop_percent)
            crop_amount_h = int(img.height * crop_percent)
            img = img.crop((
                crop_amount_w,
                crop_amount_h,
                img.width - crop_amount_w,
                img.height - crop_amount_h
            ))

        # 이미지 리사이즈
        if smallest_width != img.width:
            # 비율에 맞춰 리사이즈
            aspect_ratio = img.height / img.width
            new_height = int(smallest_width * aspect_ratio)
            img = img.resize((smallest_width, new_height), Image.LANCZOS)

        # RGB로 변환 후 리스트에 추가
        images.append(img.convert('RGB'))

    if images:
        # 첫 번째 이미지를 기반으로 PDF 생성 (JPEG 압축률 적용)
        first_image = images.pop(0)
        first_image.save(output_pdf_path, save_all=True, append_images=images, quality=jpeg_quality)

# 사용 예시
folder_paths = [
    r"C:/temp/doc1",
    r"C:/temp/doc2",
    r"C:/temp/doc3",
]
output_pdf_path = 'C:/temp/output.pdf'  # 생성될 PDF 파일 경로

jpeg_quality = 50  # JPEG 압축률 (0에서 100 사이의 값, 100이 가장 높은 품질)
crop_percent = 0.03  # 이미지 상하좌우에서 자를 비율

jpgs_to_pdf(folder_paths, output_pdf_path, jpeg_quality, crop_percent)

print(f"{output_pdf_path} 파일이 생성되었습니다.")
