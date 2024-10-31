# main.py

import cv2
import mediapipe as mp
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import math

# =========================
# 1. 상수 및 설정값
# =========================

# 부정행위로 간주할 지속 시간 (초)
CHEATING_THRESHOLD = 3  # 3초 이상 지속 시 부정행위로 판단

# 머리 회전 각도 기준치
HEAD_TURN_THRESHOLD = 20  # 각도 절댓값이 20도 이상이면 고개를 돌린 것으로 판단

# 눈동자 각도 기준치
EYE_TURN_THRESHOLD = 20  # 정면 기준 좌우 20도 이상이면 눈동자를 돌린 것으로 판단

# 프레임 샘플링 간격 설정
FRAME_SAMPLING_INTERVAL = 5  # 원하는 샘플링 간격으로 설정 (예: 5)

# 한글 폰트 경로 설정
# font = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', font_size)  # Windows의 경우
font_path = '/Library/Fonts/AppleGothic.ttf'  # MacOS의 경우

# =========================
# 2. 유틸리티 함수
# =========================

def draw_text_korean(image, text, position, font_size=30, font_color=(0, 0, 255)):
    # OpenCV 이미지를 PIL 이미지로 변환
    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(image_pil)

    # 폰트 설정
    font = ImageFont.truetype(font_path, font_size)

    # 텍스트 그리기
    draw.text(position, text, font=font, fill=font_color)

    # PIL 이미지를 OpenCV 이미지로 변환
    image = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
    return image

def calculate_head_pose(landmarks, image_shape):
    # 3D 모델 포인트 설정
    model_points = np.array([
        (0.0, 0.0, 0.0),             # 코 끝: 1번 랜드마크
        (0.0, -330.0, -65.0),        # 턱 끝: 152번 랜드마크
        (-225.0, 170.0, -135.0),     # 왼쪽 눈 좌측 끝: 33번 랜드마크
        (225.0, 170.0, -135.0),      # 오른쪽 눈 우측 끝: 263번 랜드마크
        (-150.0, -150.0, -125.0),    # 입 좌측 끝: 78번 랜드마크
        (150.0, -150.0, -125.0)      # 입 우측 끝: 308번 랜드마크
    ])

    image_points = np.array([
        (landmarks.landmark[1].x * image_shape[1], landmarks.landmark[1].y * image_shape[0]),    # 코 끝
        (landmarks.landmark[152].x * image_shape[1], landmarks.landmark[152].y * image_shape[0]),  # 턱 끝
        (landmarks.landmark[33].x * image_shape[1], landmarks.landmark[33].y * image_shape[0]),   # 왼쪽 눈 좌측 끝
        (landmarks.landmark[263].x * image_shape[1], landmarks.landmark[263].y * image_shape[0]),  # 오른쪽 눈 우측 끝
        (landmarks.landmark[78].x * image_shape[1], landmarks.landmark[78].y * image_shape[0]),   # 입 좌측 끝
        (landmarks.landmark[308].x * image_shape[1], landmarks.landmark[308].y * image_shape[0])  # 입 우측 끝
    ], dtype='double')

    # 카메라 매트릭스 설정
    focal_length = image_shape[1]
    center = (image_shape[1] / 2, image_shape[0] / 2)
    camera_matrix = np.array(
        [[focal_length, 0, center[0]],
         [0, focal_length, center[1]],
         [0, 0, 1]], dtype='double')

    dist_coeffs = np.zeros((4, 1))  # 왜곡 계수는 0으로 설정

    # SolvePnP를 사용하여 회전 및 변환 벡터 계산
    success, rotation_vector, translation_vector = cv2.solvePnP(
        model_points, image_points, camera_matrix, dist_coeffs)

    # 회전 벡터를 오일러 각도로 변환
    rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
    pose_matrix = cv2.hconcat((rotation_matrix, translation_vector))
    _, _, _, _, _, _, euler_angles = cv2.decomposeProjectionMatrix(pose_matrix)

    pitch, yaw, roll = [angle[0] for angle in euler_angles]

    return pitch, yaw, roll

def calculate_eye_direction(landmarks, image_shape):
    # 왼쪽 및 오른쪽 눈동자 중심 계산
    h, w = image_shape[:2]

    left_eye = landmarks.landmark[468]  # 왼쪽 눈동자 중심
    right_eye = landmarks.landmark[473]  # 오른쪽 눈동자 중심

    left_eye_point = np.array([left_eye.x * w, left_eye.y * h])
    right_eye_point = np.array([right_eye.x * w, right_eye.y * h])

    # 눈동자 중심의 평균 좌표 계산
    eyes_center = (left_eye_point + right_eye_point) / 2

    # 코 끝 좌표 추출
    nose_tip = landmarks.landmark[1]
    nose_point = np.array([nose_tip.x * w, nose_tip.y * h])

    # 시선 벡터 계산
    gaze_vector = eyes_center - nose_point

    # 시선 방향 계산 (각도)
    dx = gaze_vector[0]
    dy = -gaze_vector[1]  # y축 반전

    angle = math.degrees(math.atan2(dy, dx))
    if angle < 0:
        angle += 360

    return angle

def detect_hand_gesture(hand_landmarks):
    # 손가락이 펴져 있는지 확인하여 특정 제스처를 인식
    # 엄지, 검지, 중지, 약지, 소지에 대한 랜드마크 인덱스
    finger_tips = [4, 8, 12, 16, 20]
    finger_pip = [3, 7, 11, 15, 19]

    fingers_status = []

    for tip, pip in zip(finger_tips, finger_pip):
        tip_y = hand_landmarks.landmark[tip].y
        pip_y = hand_landmarks.landmark[pip].y

        if tip_y < pip_y:
            fingers_status.append(1)  # 손가락 펴짐
        else:
            fingers_status.append(0)  # 손가락 구부러짐

    # 모든 손가락이 펴져 있으면 특정 제스처로 판단
    if sum(fingers_status) == 5:
        return True  # 부정행위 제스처 감지
    else:
        return False

# =========================
# 3. 부정행위 감지 함수
# =========================

def detect_face_absence(face_present, start_times, cheating_flags, cheating_counts):
    current_time = time.time()
    if not face_present:
        if start_times['face'] is None:
            start_times['face'] = current_time
        else:
            elapsed_time = current_time - start_times['face']
            if elapsed_time >= CHEATING_THRESHOLD and not cheating_flags['face']:
                cheating_flags['face'] = True
                cheating_counts['face'] += 1
                current_time_str = time.strftime("%Y-%m-%d %H:%M:%S")
                print(f'부정행위 감지! 유형: 얼굴 미검출, 시간: {current_time_str}, 횟수: {cheating_counts["face"]}')
    else:
        start_times['face'] = None
        cheating_flags['face'] = False

def detect_head_turn(yaw, start_times, cheating_flags, cheating_counts):
    current_time = time.time()
    if abs(yaw) > HEAD_TURN_THRESHOLD:
        if start_times['head'] is None:
            start_times['head'] = current_time
        else:
            elapsed_time = current_time - start_times['head']
            if elapsed_time >= CHEATING_THRESHOLD and not cheating_flags['head']:
                cheating_flags['head'] = True
                cheating_counts['head'] += 1
                current_time_str = time.strftime("%Y-%m-%d %H:%M:%S")
                print(f'부정행위 감지! 유형: 고개 돌림, 시간: {current_time_str}, 횟수: {cheating_counts["head"]}')
    else:
        start_times['head'] = None
        cheating_flags['head'] = False

def detect_eye_movement(eye_angle, start_times, cheating_flags, cheating_counts):
    current_time = time.time()
    if eye_angle < (90 - EYE_TURN_THRESHOLD) or eye_angle > (90 + EYE_TURN_THRESHOLD):
        if start_times['eye'] is None:
            start_times['eye'] = current_time
        else:
            elapsed_time = current_time - start_times['eye']
            if elapsed_time >= CHEATING_THRESHOLD and not cheating_flags['eye']:
                cheating_flags['eye'] = True
                cheating_counts['eye'] += 1
                current_time_str = time.strftime("%Y-%m-%d %H:%M:%S")
                print(f'부정행위 감지! 유형: 눈동자 돌림, 시간: {current_time_str}, 횟수: {cheating_counts["eye"]}')
    else:
        start_times['eye'] = None
        cheating_flags['eye'] = False

def detect_hand_gesture_wrapper(hand_gesture_detected, hand_label, start_times, cheating_flags, cheating_counts):
    current_time = time.time()
    if hand_gesture_detected:
        if start_times['hand'].get(hand_label) is None:
            start_times['hand'][hand_label] = current_time
        else:
            elapsed_time = current_time - start_times['hand'][hand_label]
            if elapsed_time >= CHEATING_THRESHOLD and not cheating_flags['hand'].get(hand_label, False):
                cheating_flags['hand'][hand_label] = True
                cheating_counts['hand'][hand_label] = cheating_counts['hand'].get(hand_label, 0) + 1
                current_time_str = time.strftime("%Y-%m-%d %H:%M:%S")
                print(f'부정행위 감지! 유형: 손동작, 손: {hand_label}, 시간: {current_time_str}, 횟수: {cheating_counts["hand"][hand_label]}')
    else:
        start_times['hand'][hand_label] = None
        cheating_flags['hand'][hand_label] = False

# =========================
# 4. 메인 실행 부분
# =========================

def main():
    # MediaPipe 초기화
    mp_face_mesh = mp.solutions.face_mesh
    mp_face_detection = mp.solutions.face_detection
    mp_hands = mp.solutions.hands

    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
    hands = mp_hands.Hands(
        max_num_hands=2,  # 두 손 인식을 위해 2로 설정
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    # 그리기 유틸리티
    mp_drawing = mp.solutions.drawing_utils

    # 부정행위 관련 변수 초기화
    start_times = {'head': None, 'eye': None, 'face': None, 'hand': {}}
    cheating_flags = {'head': False, 'eye': False, 'face': False, 'hand': {}}
    cheating_counts = {'head': 0, 'eye': 0, 'face': 0, 'hand': {}}

    frame_count = 0  # 프레임 카운터 변수 추가

    # 웹캠 열기
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("카메라에서 프레임을 읽을 수 없습니다.")
            break

        frame_count += 1  # 프레임 카운터 증가

        # 프레임 샘플링: 지정한 간격의 프레임만 처리
        if frame_count % FRAME_SAMPLING_INTERVAL != 0:
            continue  # 다음 프레임으로 넘어감

        # 성능 향상을 위해 이미지 쓰기 권한 해제
        image.flags.writeable = False
        # BGR 이미지를 RGB로 변환
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 얼굴 검출
        face_results = face_detection.process(image_rgb)
        face_present = False if not face_results.detections else True

        # 얼굴 부정행위 감지
        detect_face_absence(face_present, start_times, cheating_flags, cheating_counts)

        # 얼굴 랜드마크 추출
        face_mesh_results = face_mesh.process(image_rgb)

        # 손 랜드마크 추출
        hands_results = hands.process(image_rgb)

        # 이미지 쓰기 권한 재설정
        image.flags.writeable = True
        # RGB 이미지를 BGR로 변환
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        if face_mesh_results.multi_face_landmarks:
            face_landmarks = face_mesh_results.multi_face_landmarks[0]

            # 머리 자세 추정
            pitch, yaw, roll = calculate_head_pose(face_landmarks, image.shape)

            # 머리 부정행위 감지
            detect_head_turn(yaw, start_times, cheating_flags, cheating_counts)

            # 눈동자 움직임 추적
            eye_angle = calculate_eye_direction(face_landmarks, image.shape)

            # 눈동자 부정행위 감지
            detect_eye_movement(eye_angle, start_times, cheating_flags, cheating_counts)

            # 얼굴 랜드마크 그리기 (디버깅용)
            mp_drawing.draw_landmarks(
                image, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
            )

            # 머리 자세 정보 표시
            text = f'Yaw(좌우): {yaw:.1f}, Pitch(상하): {pitch:.1f}, Roll(기울기): {roll:.1f}'
            image = draw_text_korean(image, text, (30, 30), font_size=20, font_color=(255, 255, 255))

        else:
            # 얼굴 랜드마크가 검출되지 않는 경우
            start_times['head'] = None
            cheating_flags['head'] = False
            start_times['eye'] = None
            cheating_flags['eye'] = False

        # 손동작 감지
        if hands_results.multi_hand_landmarks:
            for hand_landmarks, hand_info in zip(hands_results.multi_hand_landmarks, hands_results.multi_handedness):
                hand_label = hand_info.classification[0].label  # 'Left' 또는 'Right'

                # 부정행위 관련 변수 초기화
                if hand_label not in start_times['hand']:
                    start_times['hand'][hand_label] = None
                    cheating_flags['hand'][hand_label] = False
                    cheating_counts['hand'][hand_label] = 0

                # 부정행위 제스처 감지
                hand_gesture_detected = detect_hand_gesture(hand_landmarks)

                # 손동작 부정행위 감지
                detect_hand_gesture_wrapper(hand_gesture_detected, hand_label, start_times, cheating_flags, cheating_counts)

                # 손 랜드마크 그리기 (디버깅용)
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
                )
        else:
            start_times['hand'] = {}
            cheating_flags['hand'] = {}

        # 부정행위 상태 표시
        status_text = ''
        if cheating_flags['face']:
            status_text += '부정행위 감지: 얼굴 미검출\n'
        if cheating_flags['head']:
            status_text += '부정행위 감지: 고개 돌림\n'
        if cheating_flags['eye']:
            status_text += '부정행위 감지: 눈동자 돌림\n'
        for hand_label, flag in cheating_flags['hand'].items():
            if flag:
                status_text += f'부정행위 감지: 손동작 (손: {hand_label})\n'
        if status_text == '':
            status_text = '정상 상태'

        # 상태 표시
        y0, dy = 60, 30
        for i, line in enumerate(status_text.strip().split('\n')):
            y = y0 + i * dy
            image = draw_text_korean(
                image,
                line,
                (30, y),
                font_size=20,
                font_color=(0, 0, 255) if '부정행위' in line else (0, 255, 0)
            )

        # 결과 이미지 출력
        cv2.imshow('Gaze and Motion Tracking', image)

        if cv2.waitKey(5) & 0xFF == 27:  # ESC 키를 누르면 종료
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()