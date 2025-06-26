"""
2025.6.26
计算图像分割任务中类别[0,1,2,3]的预测结果与真实标签之间的 Dice 系数和 IoU（交并比）
根据情况修改：pred_label_dir、true_label_dir、image_dir
"""

import os
import cv2
import numpy as np

# 定义预测标签和真实标签的文件夹路径
pred_label_dir = r"E:\remote\Yolo\test_pred_result\arthroscopy_seg_seg2_pred_largertest\labels"
true_label_dir = r"E:\remote\Yolo\arthroscopy_dataset\labels\test"
image_dir = r"E:\remote\Yolo\arthroscopy_dataset\images\test"

# 存储每个类别的交集、面积和、并集的像素数量
class_intersection = {i: 0 for i in [0, 1, 2, 3]}
class_area_sum = {i: 0 for i in [0, 1, 2, 3]}
class_union = {i: 0 for i in [0, 1, 2, 3]}

# 遍历预测标签文件夹中的所有 txt 文件
for txt_file in os.listdir(pred_label_dir):
    if txt_file.endswith('.txt'):
        pred_txt_path = os.path.join(pred_label_dir, txt_file)
        true_txt_path = os.path.join(true_label_dir, txt_file)
        image_name = txt_file.replace('.txt', '.png')
        image_path = os.path.join(image_dir, image_name)

        # 检查对应的真实标签文件和图片文件是否存在
        if not os.path.exists(true_txt_path) or not os.path.exists(image_path):
            continue

        # 读取图片获取尺寸
        image = cv2.imread(image_path)
        image_height, image_width = image.shape[:2]

        # 初始化每个类别的预测掩码和真实掩码
        pred_masks = {i: np.zeros((image_height, image_width), dtype=np.uint8) for i in [0, 1, 2, 3]}
        true_masks = {i: np.zeros((image_height, image_width), dtype=np.uint8) for i in [0, 1, 2, 3]}

        # 处理预测标签文件
        with open(pred_txt_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                class_id = int(parts[0])
                if class_id not in [0, 1, 2, 3]:
                    continue
                segmentation_points = np.array([float(x) for x in parts[1:-1]], dtype=np.float32)
                if len(segmentation_points) % 2 != 0:
                    print('line:', line)
                    continue
                segmentation_points = segmentation_points.reshape(-1, 2)
                segmentation_points[:, 0] *= image_width
                segmentation_points[:, 1] *= image_height
                segmentation_points = segmentation_points.astype(np.int32)
                cv2.fillPoly(pred_masks[class_id], [segmentation_points], 255)

        # 处理真实标签文件
        with open(true_txt_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                class_id = int(parts[0])
                if class_id not in [0, 1, 2, 3]:
                    continue
                segmentation_points = np.array([float(x) for x in parts[1:]], dtype=np.float32)
                if len(segmentation_points) % 2 != 0:
                    print('line:', line)
                    continue
                segmentation_points = segmentation_points.reshape(-1, 2)
                segmentation_points[:, 0] *= image_width
                segmentation_points[:, 1] *= image_height
                segmentation_points = segmentation_points.astype(np.int32)
                cv2.fillPoly(true_masks[class_id], [segmentation_points], 255)

        # 计算每个类别的交集、面积和、并集
        for class_id in [0, 1, 2, 3]:
            pred_class_mask = (pred_masks[class_id] == 255).astype(np.uint8)
            true_class_mask = (true_masks[class_id] == 255).astype(np.uint8)
            intersection = np.sum(pred_class_mask & true_class_mask)
            pred_area = np.sum(pred_class_mask)
            true_area = np.sum(true_class_mask)
            area_sum = pred_area + true_area
            union = np.sum(pred_class_mask | true_class_mask)

            class_intersection[class_id] += intersection
            class_area_sum[class_id] += area_sum
            class_union[class_id] += union

# 计算每个类别的 Dice 值
total_intersection = 0
total_area_sum = 0
total_union = 0
for class_id in [0, 1, 2, 3]:
    dice = 2 * class_intersection[class_id] / (class_area_sum[class_id] + 1e-6)
    iou = class_intersection[class_id] / (class_union[class_id] + 1e-6)
    print(f"类别 {class_id} 的 Dice 值: {dice:.4f}")
    print(f"类别 {class_id} 的 IoU 值: {iou:.4f}")
    total_intersection += class_intersection[class_id]
    total_area_sum += class_area_sum[class_id]
    total_union += class_union[class_id]

# 计算总体 Dice 值和 IoU 值
total_dice = 2 * total_intersection / (total_area_sum + 1e-6)
total_iou = total_intersection / (total_union + 1e-6)
print(f"总体 Dice 值: {total_dice:.4f}")
print(f"总体 IoU 值: {total_iou:.4f}")
