import os
from PIL import Image
from rembg import remove, new_session

def remove_background_and_save(source_folder, destination_folder, model_name):
    # 세션 객체 생성, 특정 모델 지정
    session = new_session(model_name=model_name)

    # 소스 폴더에서 모든 파일을 검색
    for filename in os.listdir(source_folder):
        if filename.endswith('.webp') or filename.endswith('.jpg') \
                or filename.endswith('.png') or filename.endswith('.jpeg'):
            file_path = os.path.join(source_folder, filename)
            output_filename = os.path.splitext(filename)[0] + '.png'  # 원래 파일 이름에서 확장자를 png로 변경
            output_path = os.path.join(destination_folder, output_filename)
            print(file_path)
            if os.path.exists(output_path):
                print(f"File {output_path} already exists, skipping...")
                continue

            # 이미지 파일을 열고 배경 제거
            with Image.open(file_path) as img:
                input_data = img.convert("RGBA")  # rembg는 RGBA 포맷의 바이트 데이터가 필요

                # alpha_matting_foreground_threshold: 알파 매팅에서 전경 임계값을 설정합니다. 기본값은 240입니다.
                # alpha_matting_background_threshold: 알파 매팅에서 배경 임계값을 설정합니다. 기본값은 10입니다.
                result_data = remove(input_data, session=session, alpha_matting=True,
                                     alpha_matting_background_threshold=128) # 배경 제거

                # 결과 이미지 생성 및 저장
                result_data.save(output_path, format='PNG')  # PNG 형식으로 저장


if __name__ == "__main__":
    # 폴더 경로 설정 (사용자가 수정 가능)
    source_folder = r'D:\dev\game_art\dalle\monster'
    destination_folder = r'D:\dev\game_art\dalle\monster\rbg'

    model_name = 'birefnet-general'  # 'u2net', 'u2net_human_seg' 등 다른 모델도 사용 가능

    '''
    The available models are:

    u2net (download, source): A pre-trained model for general use cases.
    u2netp (download, source): A lightweight version of u2net model.
    u2net_human_seg (download, source): A pre-trained model for human segmentation.
    u2net_cloth_seg (download, source): A pre-trained model for Cloths Parsing from human portrait. 
                      Here clothes are parsed into 3 category: Upper body, Lower body and Full body.
    silueta (download, source): Same as u2net but the size is reduced to 43Mb.
    isnet-general-use (download, source): A new pre-trained model for general use cases.
    isnet-anime (download, source): A high-accuracy segmentation for anime character.
    sam (download encoder, download decoder, source): A pre-trained model for any use cases.
    birefnet-general (download, source): A pre-trained model for general use cases.
    birefnet-general-lite (download, source): A light pre-trained model for general use cases.
    birefnet-portrait (download, source): A pre-trained model for human portraits.
    birefnet-dis (download, source): A pre-trained model for dichotomous image segmentation (DIS).
    birefnet-hrsod (download, source): A pre-trained model for high-resolution salient object detection (HRSOD).
    birefnet-cod (download, source): A pre-trained model for concealed object detection (COD).
    birefnet-massive (download, source): A pre-trained model with massive dataset.
    '''

    # 경로가 없다면 생성
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    remove_background_and_save(source_folder, destination_folder, model_name)
