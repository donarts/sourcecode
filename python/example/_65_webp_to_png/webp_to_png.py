from PIL import Image
import os

# 설정 변수
input_folder = r'D:\dev\game_art\dalle\card'  # 웹피 파일들이 위치한 입력 폴더
output_folder = r'D:\dev\game_art\dalle\card_210'  # PNG 파일들을 저장할 출력 폴더
size = (210, 210)  # 리사이즈할 크기 (너비, 높이)

# 입력 폴더가 존재하지 않으면 예외 발생
if not os.path.exists(input_folder):
    raise FileNotFoundError(f"입력 폴더 '{input_folder}' 가 존재하지 않습니다.")

# 출력 폴더가 존재하지 않으면 생성
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 입력 폴더에서 모든 웹피 파일을 찾아 처리
for filename in os.listdir(input_folder):
    if filename.endswith('.webp'):
        # 원본 파일 경로
        original_path = os.path.join(input_folder, filename)

        # 이미지 열기
        with Image.open(original_path) as img:
            # 이미지 리사이즈
            img_resized = img.resize(size, Image.Resampling.LANCZOS)

            # 출력 파일 경로 (.webp -> .png)
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.png')

            # 이미지 저장
            img_resized.save(output_path, 'PNG')

print("모든 파일이 처리되었습니다.")