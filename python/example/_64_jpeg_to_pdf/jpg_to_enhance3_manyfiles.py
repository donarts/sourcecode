import cv2
import numpy as np
import os

def process_image(input_image_path, output_image_path, crop_percent=0.05, jpeg_quality=95):
    # 이미지 불러오기
    image = cv2.imread(input_image_path)
    height, width = image.shape[:2]

    # 상하좌우 crop_percent 부분 제거
    crop_top = int(crop_percent * height)
    crop_bottom = int((1 - crop_percent) * height)
    crop_left = int(crop_percent * width)
    crop_right = int((1 - crop_percent) * width)
    cropped_image = image[crop_top:crop_bottom, crop_left:crop_right]

    image_rgb = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)

    # 1. 샤프닝 적용
    kernel_sharpen = np.array([[-1, -1, -1],
                               [-1, 9, -1],
                               [-1, -1, -1]])
    sharpened_image = cv2.filter2D(image_rgb, -1, kernel_sharpen)

    # 2. bilateralFilter 적용
    bilateral_filtered_image = cv2.bilateralFilter(sharpened_image, d=9, sigmaColor=75, sigmaSpace=75)

    # 3. Grayscale 변환
    gray = cv2.cvtColor(bilateral_filtered_image, cv2.COLOR_RGB2GRAY)

    # 4. GaussianBlur 적용 (Thresholding 전에)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive Thresholding을 사용하여 글씨와 배경 분리
    mask = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY_INV, 41, 8)

    # 배경 마스크를 생성 (글씨가 있는 부분은 제외)
    background_mask = cv2.bitwise_not(mask)

    # 배경을 밝게 조정 (50 정도 밝기 증가)
    background_brightened = cv2.add(bilateral_filtered_image, np.array([50.0, 50.0, 50.0], dtype=np.float32), mask=background_mask)

    # 글씨 부분은 원본에서 그대로 가져옵니다.
    final_image = cv2.add(background_brightened, cv2.bitwise_and(bilateral_filtered_image, bilateral_filtered_image, mask=mask))

    # RGB 이미지를 다시 BGR로 변환하여 저장 (OpenCV는 BGR 형식 사용)
    final_image_bgr = cv2.cvtColor(final_image, cv2.COLOR_RGB2BGR)

    # 변환된 이미지를 JPG로 저장하면서 압축률 설정
    cv2.imwrite(output_image_path, final_image_bgr, [cv2.IMWRITE_JPEG_QUALITY, jpeg_quality])

def process_images_in_folder(input_folder, output_folder, crop_percent=0.05, jpeg_quality=95):
    # 입력 폴더 내의 모든 파일에 대해 작업 수행
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
            input_image_path = os.path.join(input_folder, filename)
            output_image_path = os.path.join(output_folder, filename)

            # 이미지 처리 및 저장
            process_image(input_image_path, output_image_path, crop_percent, jpeg_quality)
            print(f"Processed and saved: {output_image_path} with JPEG quality {jpeg_quality}")

# 입력 및 출력 폴더 경로 설정
input_folder = r"D:/temp/input"
output_folder = r"D:/temp/output"

# 출력 폴더가 없으면 생성
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 폴더 내 모든 이미지 처리 (JPEG 압축 품질 설정 가능)
jpeg_quality = 50  # JPEG 압축률 (0에서 100 사이의 값, 100이 가장 높은 품질)
crop_percent = 0.05  # 이미지 상하좌우에서 자를 비율
process_images_in_folder(input_folder, output_folder, crop_percent, jpeg_quality)