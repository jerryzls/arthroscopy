# 2025.6.26
# 使用yolo分割预测的txt文件，在原始png图片上绘制结果并显示，图片地址为image_path，txt文件地址txt_path
# txt文件中，第一个数字为class id，最后一个数字为置信度，中间的数字为分割点的坐标，坐标为归一化后的坐标，需要将其转换为实际像素坐标

import cv2
import numpy as np

# 图片和 txt 文件的路径
image_path = r"E:\remote\Yolo\arthroscopy_dataset\images\test\14.png"
txt_path = r"E:\remote\Yolo\test_pred_result\arthroscopy_seg_pred\labels\14.txt"
# txt_path = r"E:\remote\Yolo\arthroscopy_dataset\labels\test\5.txt"

# 读取图片
image = cv2.imread(image_path)
image_height, image_width = image.shape[:2]

# 读取 txt 文件
with open(txt_path, 'r') as f:
    lines = f.readlines()

# 遍历每一行预测结果
for line in lines:
    parts = line.strip().split()
    class_id = int(parts[0])
    # 提取分割点的坐标，跳过类别 ID
    segmentation_points = np.array([float(x) for x in parts[1:-1]], dtype=np.float32)
    # 将归一化的坐标转换为实际像素坐标
    segmentation_points = segmentation_points.reshape(-1, 2)
    segmentation_points[:, 0] *= image_width
    segmentation_points[:, 1] *= image_height
    segmentation_points = segmentation_points.astype(np.int32)

    # 随机生成颜色
    color = tuple(np.random.randint(0, 256, 3).tolist())
    # 绘制分割掩码
    cv2.fillPoly(image, [segmentation_points], color)
    # 绘制轮廓
    cv2.polylines(image, [segmentation_points], isClosed=True, color=(0, 0, 0), thickness=2)

# 显示图片
cv2.imshow("Segmentation Result", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
