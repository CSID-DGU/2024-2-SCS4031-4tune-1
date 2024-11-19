import time
import cv2
from constants import *
from custom_utils import *

def detect_look_around(user_id, pitch, yaw, start_times, cheating_flags, cheating_counts, cheating_messages):
    current_time = time.time()
    if pitch <= PITCH_DOWN_THRESHOLD and abs(yaw) > YAW_FORWARD_THRESHOLD:
        if start_times[user_id]['look_around'] is None:
            start_times[user_id]['look_around'] = current_time
        else:
            elapsed_time = current_time - start_times[user_id]['look_around']
            if elapsed_time >= LOOK_AROUND_THRESHOLD and not cheating_flags[user_id]['look_around']:
                cheating_flags[user_id]['look_around'] = True
                cheating_counts[user_id]['look_around'] += 1
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
                message = {'type': '주변 응시', 'start_time': current_time}
                cheating_messages[user_id].append(message)
                print(f'[{timestamp}] User: {user_id}, 유형: 주변 응시, 횟수: {cheating_counts[user_id]["look_around"]}')
    else:
        if cheating_flags[user_id]['look_around']:
            cheating_flags[user_id]['look_around'] = False
            start_times[user_id]['look_around'] = None

def detect_repeated_gaze(user_id, grid_position, gaze_history, start_times, cheating_flags, cheating_counts, cheating_messages, pitch):
    current_time = time.time()
    if pitch <= PITCH_DOWN_THRESHOLD:
        gaze_history[user_id].append((grid_position, current_time))
        # 30초 이내의 기록만 유지
        gaze_history[user_id][:] = [(pos, t) for pos, t in gaze_history[user_id] if current_time - t <= REPEATED_GAZE_WINDOW]

        # 특정 위치에서 3초 이상 응시한 횟수 카운트
        position_times = {}
        for pos, t in gaze_history[user_id]:
            if pos not in position_times:
                position_times[pos] = [t]
            else:
                position_times[pos].append(t)

        repeated_gaze_count = 0
        for pos, times in position_times.items():
            times.sort()
            for i in range(len(times) - 1):
                if times[i+1] - times[i] <= REPEATED_GAZE_DURATION:
                    repeated_gaze_count += 1
                    break  # 해당 위치에서 한 번만 카운트

        if repeated_gaze_count >= REPEATED_GAZE_COUNT and not cheating_flags[user_id]['repeated_gaze']:
            cheating_flags[user_id]['repeated_gaze'] = True
            cheating_counts[user_id]['repeated_gaze'] += 1
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
            message = {'type': '동일 위치 반복 응시', 'start_time': current_time}
            cheating_messages[user_id].append(message)
            print(f'[{timestamp}] User: {user_id}, 유형: 동일 위치 반복 응시, 횟수: {cheating_counts[user_id]["repeated_gaze"]}')
    else:
        if cheating_flags[user_id]['repeated_gaze']:
            cheating_flags[user_id]['repeated_gaze'] = False
            start_times[user_id]['repeated_gaze'] = None

def detect_object_presence(user_id, detections, cheating_flags, cheating_counts, cheating_messages, image):
    current_time = time.time()
    cheating_objects_detected = [d for d in detections if d['name'] in CHEATING_OBJECTS]
    if cheating_objects_detected:
        if not cheating_flags[user_id]['object']:
            cheating_flags[user_id]['object'] = True
            cheating_counts[user_id]['object'] += 1
            objects = [d['name'] for d in cheating_objects_detected]
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
            message = {'type': '부정행위 물체 감지', 'start_time': current_time}
            cheating_messages[user_id].append(message)
            print(f'[{timestamp}] User: {user_id}, 유형: 부정행위 물체 감지 ({objects}), 횟수: {cheating_counts[user_id]["object"]}')
    else:
        if cheating_flags[user_id]['object']:
            cheating_flags[user_id]['object'] = False

def detect_face_absence(user_id, face_present, start_times, cheating_flags, cheating_counts, face_absence_history, cheating_messages):
    current_time = time.time()
    if not face_present:
        if start_times[user_id]['face_absence'] is None:
            start_times[user_id]['face_absence'] = current_time
        else:
            elapsed_time = current_time - start_times[user_id]['face_absence']
            if elapsed_time >= FACE_ABSENCE_THRESHOLD and not cheating_flags[user_id]['face_absence_long']:
                cheating_flags[user_id]['face_absence_long'] = True
                cheating_counts[user_id]['face_absence_long'] += 1
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
                message = {'type': '장기 화면 이탈', 'start_time': current_time}
                cheating_messages[user_id].append(message)
                print(f'[{timestamp}] User: {user_id}, 유형: 장기 화면 이탈, 횟수: {cheating_counts[user_id]["face_absence_long"]}')
            elif elapsed_time >= FACE_ABSENCE_DURATION:
                # 3초 이상 이탈한 경우 기록
                face_absence_history[user_id].append(current_time)
                # 30초 이내의 기록만 유지
                face_absence_history[user_id][:] = [t for t in face_absence_history[user_id] if current_time - t <= FACE_ABSENCE_WINDOW]
                if len(face_absence_history[user_id]) >= FACE_ABSENCE_COUNT_THRESHOLD and not cheating_flags[user_id]['face_absence_repeat']:
                    cheating_flags[user_id]['face_absence_repeat'] = True
                    cheating_counts[user_id]['face_absence_repeat'] += 1
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
                    message = {'type': '반복 화면 이탈', 'start_time': current_time}
                    cheating_messages[user_id].append(message)
                    print(f'[{timestamp}] User: {user_id}, 유형: 반복 화면 이탈, 횟수: {cheating_counts[user_id]["face_absence_repeat"]}')
    else:
        if cheating_flags[user_id]['face_absence_long'] or cheating_flags[user_id]['face_absence_repeat']:
            cheating_flags[user_id]['face_absence_long'] = False
            cheating_flags[user_id]['face_absence_repeat'] = False
            start_times[user_id]['face_absence'] = None

def detect_hand_gestures(user_id, hand_landmarks_list, start_times, cheating_flags, cheating_counts, cheating_messages):
    current_time = time.time()
    hand_gesture_detected = False

    for hand_landmarks in hand_landmarks_list:
        gesture = recognize_hand_gesture(hand_landmarks)
        if gesture != 'fist' and gesture != 'palm':
            hand_gesture_detected = True
            if start_times[user_id]['hand_gesture'] is None:
                start_times[user_id]['hand_gesture'] = current_time
            else:
                elapsed_time = current_time - start_times[user_id]['hand_gesture']
                if elapsed_time >= HAND_GESTURE_THRESHOLD and not cheating_flags[user_id]['hand_gesture']:
                    cheating_flags[user_id]['hand_gesture'] = True
                    cheating_counts[user_id]['hand_gesture'] += 1
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
                    message = {'type': '특정 손동작 반복', 'start_time': current_time}
                    cheating_messages[user_id].append(message)
                    print(f'[{timestamp}] User: {user_id}, 부정행위 감지! 유형: 특정 손동작 반복, 횟수: {cheating_counts[user_id]["hand_gesture"]}')
        else:
            start_times[user_id]['hand_gesture'] = None
            cheating_flags[user_id]['hand_gesture'] = False

    if not hand_gesture_detected:
        start_times[user_id]['hand_gesture'] = None
        cheating_flags[user_id]['hand_gesture'] = False

def detect_head_turn(user_id, pitch, yaw, start_times, cheating_flags, cheating_counts, head_turn_history, cheating_messages):
    current_time = time.time()
    if abs(yaw) > HEAD_TURN_THRESHOLD:
        if start_times[user_id]['head_turn'] is None:
            start_times[user_id]['head_turn'] = current_time
        else:
            elapsed_time = current_time - start_times[user_id]['head_turn']
            if elapsed_time >= HEAD_TURN_DURATION and not cheating_flags[user_id]['head_turn_long']:
                cheating_flags[user_id]['head_turn_long'] = True
                cheating_counts[user_id]['head_turn_long'] += 1
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
                message = {'type': '고개 돌림 유지', 'start_time': current_time}
                cheating_messages[user_id].append(message)
                print(f'[{timestamp}] User: {user_id}, 유형: 고개 돌림 유지, 횟수: {cheating_counts[user_id]["head_turn_long"]}')
            elif elapsed_time >= HEAD_TURN_REPEAT_DURATION:
                # 3초 이상 고개를 돌린 경우 기록
                head_turn_history[user_id].append(current_time)
                # 30초 이내의 기록만 유지
                head_turn_history[user_id][:] = [t for t in head_turn_history[user_id] if current_time - t <= HEAD_TURN_WINDOW]
                if len(head_turn_history[user_id]) >= HEAD_TURN_COUNT_THRESHOLD and not cheating_flags[user_id]['head_turn_repeat']:
                    cheating_flags[user_id]['head_turn_repeat'] = True
                    cheating_counts[user_id]['head_turn_repeat'] += 1
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
                    message = {'type': '고개 돌림 반복', 'start_time': current_time}
                    cheating_messages[user_id].append(message)
                    print(f'[{timestamp}] User: {user_id}, 유형: 고개 돌림 반복, 횟수: {cheating_counts[user_id]["head_turn_repeat"]}')
    else:
        if cheating_flags[user_id]['head_turn_long'] or cheating_flags[user_id]['head_turn_repeat']:
            cheating_flags[user_id]['head_turn_long'] = False
            cheating_flags[user_id]['head_turn_repeat'] = False
            start_times[user_id]['head_turn'] = None

def detect_eye_movement(user_id, eye_center, image_shape, start_times, cheating_flags, cheating_counts, cheating_messages):
    current_time = time.time()

    # 시선이 중앙에서 얼마나 벗어났는지 계산
    image_center = (image_shape[1] // 2, image_shape[0] // 2)
    dx = eye_center[0] - image_center[0]

    # 눈동자가 좌우로 많이 움직였는지 판단
    if abs(dx) > EYE_MOVEMENT_THRESHOLD:
        if start_times[user_id]['eye_movement'] is None:
            start_times[user_id]['eye_movement'] = current_time
        else:
            elapsed_time = current_time - start_times[user_id]['eye_movement']
            if elapsed_time >= 2 and not cheating_flags[user_id]['eye_movement']:
                cheating_flags[user_id]['eye_movement'] = True
                cheating_counts[user_id]['eye_movement'] += 1
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
                message = {'type': '눈동자 움직임', 'start_time': current_time}
                cheating_messages[user_id].append(message)
                print(f'[{timestamp}] User: {user_id}, 유형: 눈동자 움직임, 횟수: {cheating_counts[user_id]["eye_movement"]}')
    else:
        if cheating_flags[user_id]['eye_movement']:
            cheating_flags[user_id]['eye_movement'] = False
            start_times[user_id]['eye_movement'] = None