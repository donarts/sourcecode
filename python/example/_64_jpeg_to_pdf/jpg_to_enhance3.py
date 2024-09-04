filename=r'D:\temp\1\0676.jpg'

import cv2
import numpy as np
import matplotlib.pyplot as plt

# 이미지 불러오기
image = cv2.imread(filename)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 1. 샤프닝 적용
kernel_sharpen = np.array([[-1, -1, -1],
                           [-1, 9, -1],
                           [-1, -1, -1]])
sharpened_image = cv2.filter2D(image_rgb, -1, kernel_sharpen)

# 2. bilateralFilter 적용
bilateral_filtered_image = cv2.bilateralFilter(sharpened_image, d=9, sigmaColor=75, sigmaSpace=75)

# 3. Grayscale 변환
gray = cv2.cvtColor(bilateral_filtered_image, cv2.COLOR_RGB2GRAY)

# Otsu's Thresholding을 사용하여 글씨와 배경 분리
# Otsu's Method는 최적의 threshold 값을 자동으로 선택함
_, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# 선택된 Otsu Threshold 값 출력
otsu_threshold_value = _  # Otsu가 선택한 최적의 Threshold 값
print(f"Otsu's Threshold Value: {otsu_threshold_value}")

# 배경 마스크를 생성 (글씨가 있는 부분은 제외)
background_mask = cv2.bitwise_not(mask)

# 배경을 밝게 조정 (50 정도 밝기 증가)
upcolor = 50
background_brightened = cv2.add(bilateral_filtered_image, np.array([upcolor, upcolor, upcolor], dtype=np.float32), mask=background_mask)

# 글씨 부분은 원본에서 그대로 가져옵니다.
final_image = cv2.add(background_brightened, cv2.bitwise_and(bilateral_filtered_image, bilateral_filtered_image, mask=mask))

# 결과 출력
plt.figure(figsize=(18, 6))
plt.subplot(131), plt.imshow(image_rgb), plt.title('Original')
plt.subplot(132), plt.imshow(bilateral_filtered_image), plt.title('Sharpened + Bilateral Filtered')
plt.subplot(133), plt.imshow(final_image), plt.title('Background Brightened with Otsu Thresholding')
plt.axis('off')
plt.show()
