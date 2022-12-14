import face_recognition
import os, sys
import cv2
import numpy as np
import math
import pyrealsense2 as rs

#일치확률 계산
def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'

#얼굴인식
class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True

    def __init__(self):
        self.encode_faces()

    def encode_faces(self):
        for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f"faces/{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)
        print(self.known_face_names)

    def run_recognition(self):
        while True:

            #프레임 가져오고, 얼리인 작업 진행
            frames = pipeline.wait_for_frames()
            frames = align.process(frames)

            #프레임 가져오기
            frame = frames.first(rs.stream.color)
            depth_frame = frames.first(rs.stream.depth)

            #프레임을 못 가져왔으면 다시 가져옴
            if not frame or not depth_frame:
                continue

            #np로 전환
            color_image = np.asanyarray(frame.get_data())
            depth_array = np.asanyarray(depth_frame.get_data())

            #연산량을 줄이기 위해 해상도 낮춤
            small_frame = cv2.resize(color_image, (0, 0), fx=0.25, fy=0.25)
            
            #얼굴 찾기
            self.face_locations = face_recognition.face_locations(small_frame)
            self.face_encodings = face_recognition.face_encodings(small_frame, self.face_locations)

            self.face_names = []
            landmark_center = []
            for face_encoding in self.face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"
                confidence = '???'

                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    confidence = face_confidence(face_distances[best_match_index])

                self.face_names.append(f'{name} ({confidence})')
                face_landmarks_list = face_recognition.face_landmarks(small_frame)

                landmark_center = []
                for landmark in face_landmarks_list:
                    d = {}
                    for k in landmark:
                        d[k] = (landmark[k][2][0],landmark[k][2][1])
                    landmark_center.append(d)

                #얼굴 렌드마크 중심 위치 프린트(디버그용)
                print("LANDMARK CENTER")
                print(landmark_center)
                print("----------------")

                for c in landmark_center[0]:
                    print(landmark_center[0][c])
                    cv2.circle(color_image, (landmark_center[0][c][0]*4,landmark_center[0][c][1]*4), 2, (0, 0, 255), 2)

            self.process_current_frame = not self.process_current_frame
            
            #화면 출력
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                # 처리할때 1/4로 줄였으니 도로 곱해야 함(화면출력은 고화질)
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                fake = False
                unknown = False
                try:
                    #인간 판별용 깊이정보 수집
                    eye_depth = depth_array[int(landmark_center[0]["left_eye"][0])*4][int(landmark_center[0]["left_eye"][1])*4]*depth_scale
                    nose_depth = depth_array[int(landmark_center[0]["nose_tip"][0]+landmark_center[0]["nose_tip"][0])*2][int(landmark_center[0]["nose_bridge"][1]+landmark_center[0]["nose_tip"][1])*2]*depth_scale
                    mouth_depth = depth_array[int(landmark_center[0]["top_lip"][0])*4][int(landmark_center[0]["top_lip"][1])*4]*depth_scale
                    chin_depth = depth_array[int(landmark_center[0]["chin"][0])*4][int(landmark_center[0]["chin"][1])*4]*depth_scale

                    print("LANDMARK DEPTH")
                    print([ nose_depth, eye_depth, mouth_depth, chin_depth ])
                    print("----------------")


                    print("Fake test / 1,2: 코/눈 위치 3: 코/입 위치, 4:과한 굴곡 5:평면")
                    #인간인지 판별
                    #1. 코는 눈보다 앞에 있어야 합니다.
                    if(nose_depth != 0 and eye_depth != 0 and nose_depth >= eye_depth ):
                       print(1)
                       fake = True

                    #2 코는 눈보다 2센치는 높아야 합니다.
                    if(nose_depth != 0 and eye_depth != 0 and eye_depth - nose_depth < 0.02):
                        print(2)
                        fake = True
                        
                    #3 코는 입보다 앞에 있어야 합니다.
                    if( nose_depth != 0 and mouth_depth != 0 and mouth_depth >= nose_depth ):
                        print(3)
                        fake = True

                    #얼굴의 모든 영역이 측정 불가능하면 unknown으로 표시합니다.
                    if( nose_depth is 0 and eye_depth is 0 and mouth_depth is 0 and chin_depth is 0):
                        unknown = True

                    #4~5. 얼굴 평면 체크
                    x = max( [ nose_depth, eye_depth, mouth_depth, chin_depth ] )
                    n = min( [ nose_depth, eye_depth, mouth_depth, chin_depth ] )

                    #4.얼굴은 30센치 이상의 굴곡을 가지지 않습니다.
                    if x-n > 0.3 :
                        print(4)
                        fake=True
                    #5. 얼굴은 최소 2센치 이상의 굴곡을 가집니다.
                    if x - n < 0.02 :
                        print(5)
                        print("value: "+str(x-n))
                        fake=True
                except Exception as e:
                    print(e)
                    #이 과정에서 오류가 나면 사람이 아닌 걸로 취급합니다.
                    fake=True

                # Create the frame with the name
                print(fake)
                if fake:
                    #가짜 사람일때 로직
                    cv2.rectangle(color_image, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.rectangle(color_image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    cv2.putText(color_image, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
                else:
                    #진짜 사람일 때 로직
                    cv2.rectangle(color_image, (left, top), (right, bottom), (255, 0, 0), 2)
                    cv2.rectangle(color_image, (left, bottom - 35), (right, bottom), (255, 0, 0), cv2.FILLED)
                    cv2.putText(color_image, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

            #화면 출력
            #깊이맵을 색상으로 변환
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_array, alpha=0.03), cv2.COLORMAP_JET)

            #이미지 붙이기
            im = np.hstack((depth_colormap,color_image))
            cv2.imshow('Face Recognition', im)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) == ord('q'):
                break

        # Release handle to the webcam
        cv2.destroyAllWindows()


#Pipeline과 config생성
pipeline = rs.pipeline()
config = rs.config()

#필요 객체 생성
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

#D415 color스트림과 depth스트림 활성화(640,480)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

#Align준비작업 depth를 color에 맞춤
align_to = rs.stream.color
align = rs.align(align_to)

#pipeline 시작
profile = pipeline.start(config)


#depth scale 가져오기(단위는 미터)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: " , depth_scale)

if __name__ == '__main__':
    fr = FaceRecognition()
    fr.run_recognition()
