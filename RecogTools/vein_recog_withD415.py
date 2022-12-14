import pyrealsense2 as rs
import numpy as np
import cv2

class VeinRecognition:

    def __init__(self):
        depth_sensor = profile.get_device().first_depth_sensor()
        clipping_distance_in_meters = 0.5 #50cm
        depth_scale = depth_sensor.get_depth_scale()
        self.clipping_distance = clipping_distance_in_meters / depth_scale

    def run_recognition(self):
        try:
            while True:
                #프레임 가져오기
                frames = pipeline.wait_for_frames()
                depth_frame = frames.first(rs.stream.depth)
                color_frame = frames.first(rs.stream.color)
                ir_frame = frames.first(rs.stream.infrared)
                
                #프레임 없으면 다시 가져옴
                if not depth_frame or not color_frame or not ir_frame:
                    continue

                # 프레임->np array
                depth_image = np.asanyarray(depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())
                ir_image = np.asanyarray(ir_frame.get_data())
                
                

                data_image = depth_colormap-ir_image
                
                grey_color = 153
                #depth가 1차원이기 때문에 3차원인 색상과 맞춰줌
                depth_image_3d = np.dstack((depth_image,depth_image,depth_image))
                #depth 멀면 삭제
                bg_removed = np.where((depth_image_3d > self.clipping_distance) | (depth_image_3d <= 0), grey_color, data_image)

                # 화면 출력
                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
                images = np.vstack((np.hstack((bg_removed, depth_colormap)),np.hstack((ir_image,color_image))))
                
                cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('RealSense', images)
                if cv2.waitKey(1) == ord('q'):
                    break
        finally:
            # Stop streaming
            pipeline.stop()
    
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
config.enable_stream(rs.stream.infrared, 640, 480, rs.format.bgr8, 30)

#Align준비작업 depth를 color에 맞춤
align_to = rs.stream.color
align = rs.align(align_to)

#pipeline 시작
profile = pipeline.start(config)

if __name__ == '__main__':
    vr = VeinRecognition()
    vr.run_recognition()
