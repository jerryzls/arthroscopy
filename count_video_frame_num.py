import cv2

# 替换为你的mp4文件路径
video_file_path = r'D:\PureVue_Camera\20250312_1638_Patient滑膜炎\Video\Patient_007.mp4'

# 使用cv2.VideoCapture打开视频文件
cap = cv2.VideoCapture(video_file_path)
# print(len(cap))

# 检查是否成功打开
if not cap.isOpened():
    print("Error: Could not open video.")
else:
    # 获取视频的帧数
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    print(f"The video has {frame_count} frames.")
    print(f"The video has {fps} fps.")
    print(f"The video height is {frame_height} .")
    print(f"The video width is {frame_width} .")

# 释放视频捕获对象
cap.release()

# The video has 18484 frames.
# The video has 60.0 fps.
# The video height is 1080.0 .
# The video width is 1920.0 .
