import os

# 설정 변수
input_folder = r'D:\dev\game_art\dalle\card_210'  # 파일들이 위치한 폴더

# 폴더가 존재하지 않으면 예외 발생
if not os.path.exists(input_folder):
    raise FileNotFoundError(f"폴더 '{input_folder}' 가 존재하지 않습니다.")

# 폴더 내의 모든 파일에 대해 이름 변경 수행
for filename in os.listdir(input_folder):
    # 파일 이름에서 'for'가 시작하는 위치 찾기
    start_index = filename.find('for ')
    if start_index != -1:
        # 'for' 다음부터 ','까지의 문자열 추출
        end_index = filename.find(',', start_index)
        if end_index == -1:
            end_index = len(filename)

        # 새로운 파일 이름 생성
        new_name = filename[start_index + 4:end_index].replace(' ', '')  # 공백 제거
        extension = os.path.splitext(filename)[1]  # 원본 파일 확장자 추출
        new_filename = new_name + extension

        # 이미 존재하는 파일 이름 처리
        final_path = os.path.join(input_folder, new_filename)
        counter = 1
        while os.path.exists(final_path):
            new_filename = f"{new_name}{counter}{extension}"
            final_path = os.path.join(input_folder, new_filename)
            counter += 1

        # 파일 이름 변경
        original_path = os.path.join(input_folder, filename)
        os.rename(original_path, final_path)
        print(f"'{filename}' -> '{new_filename}'")

print("모든 파일이 변경되었습니다.")