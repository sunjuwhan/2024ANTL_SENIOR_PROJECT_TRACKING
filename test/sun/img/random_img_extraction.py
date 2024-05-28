import os
import cv2
import numpy as np
import random


def get_random_frame_from_video(video_path, output_dir):
    # 비디오 캡처 객체 생성
    cap = cv2.VideoCapture(video_path)

    # 총 프레임 수 얻기
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 랜덤 프레임 인덱스 선택
    random_frame_idx = random.randint(0, frame_count - 1)

    # 랜덤 프레임으로 이동
    cap.set(cv2.CAP_PROP_POS_FRAMES, random_frame_idx)

    # 랜덤 프레임 읽기
    ret, frame = cap.read()

    if ret:
        # 파일명과 저장 경로 설정
        video_filename = os.path.basename(video_path)
        frame_filename = f"{os.path.splitext(video_filename)[0]}_frame_{random_frame_idx}.jpg"
        frame_path = os.path.join(output_dir, frame_filename)

        # 프레임 저장
        cv2.imwrite(frame_path, frame)
    else:
        print(f"Failed to capture frame from {video_path}")

    # 비디오 캡처 객체 해제
    cap.release()


def process_videos_in_folder(data_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, dirs, files in os.walk(data_folder):
        for file in files:
            if file.endswith(".mp4"):
                video_path = os.path.join(root, file)
                get_random_frame_from_video(video_path, output_folder)
                print(f"Processed {video_path}")


# 데이터 폴더와 출력 폴더 설정
data_folder = 'C:\\Users\\ANTL\\Desktop\\drone-vis-recog-datasets-2-master\\data'  # mp4 파일이 있는 최상위 데이터 폴더
output_folder = 'C:\\Users\\ANTL\\Desktop\\GitHub\\2024ANTL_SENIOR_PROJECT_TRACKING\\test\\sun\\img'  # 랜덤 프레임이 저장될 폴더

# 비디오 처리 실행
process_videos_in_folder(data_folder, output_folder)
