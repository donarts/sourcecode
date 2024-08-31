import cv2
import os

# 특정 폴더에 있는 모든 jpg 파일들을 unshap mask하여 text의 가독성을 올립니다.

def unsharp_mask(image, sigma=1.0, strength=2):
    # 가우시안 블러를 사용하여 이미지의 블러링
    blurred = cv2.GaussianBlur(image, (0, 0), sigma)
    # 언샵 마스크 적용
    sharpened = cv2.addWeighted(image, 1 + strength, blurred, -strength, 0)
    return sharpened

def process_images(input_folder, output_folder, quality=95):
    # 출력 폴더가 존재하지 않으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 입력 폴더의 모든 JPG 파일에 대해 반복
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.jpg'):
            # 이미지 경로 설정
            img_path = os.path.join(input_folder, filename)
            # 이미지 읽기
            image = cv2.imread(img_path)

            # 이미지가 제대로 읽혔는지 확인
            if image is not None:
                # 언샵 마스크 적용
                sharpened_image = unsharp_mask(image)

                # 출력 경로 설정
                output_path = os.path.join(output_folder, filename)
                # 이미지 저장 (압축률 설정)
                cv2.imwrite(output_path, sharpened_image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
                print(f'{filename} processed and saved to {output_folder} with quality {quality}')
            else:
                print(f'Error reading image: {img_path}')

# 폴더 경로 설정
input_folder = r"D:/temp/1_20240830"
output_folder = r"D:/temp/1"
quality = 65  # JPEG 압축 품질을 설정합니다 (0-100)

# 이미지 처리 함수 호출
process_images(input_folder, output_folder, quality)