# 2025.6.25
# 对yolo训练数据集进行重复采样，使得每个类别出现的次数与其他类别大致相同

import os
import random

# 设置基础路径
base_path = r"E:/remote/Yolo/arthroscopy_dataset"
stage = 'train'

# 假设 train.txt 记录了训练集图像路径
train_file = os.path.join(base_path, f'images/{stage}.txt')
# 存储新的训练集文件路径
new_train_file = os.path.join(base_path, f'images/{stage}_balanced.txt')

# 类别标签文件路径
label_dir = os.path.join(base_path, f'labels/{stage}')

# 定义不同 class_id 的采样倍数
sampling_ratios = {1: 2.75, 2: 1.85, 3: 3.5}

# 读取原始训练集文件
with open(train_file, 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    img_path = line.strip()
    label_path = os.path.join(label_dir, os.path.basename(img_path).replace('.png', '.txt'))

    # 用于记录每个图片对应的最大重复倍数
    max_ratio = 1

    # 检查标签文件中是否包含指定类型数据
    if os.path.exists(label_path):
        with open(label_path, 'r') as label_f:
            labels = label_f.readlines()
            for label in labels:
                class_id = int(label.split()[0])
                # print('class_id:', class_id)
                if class_id in sampling_ratios:
                    # 取最大的重复倍数
                    max_ratio = max(max_ratio, sampling_ratios[class_id])
                    break

    # 计算重复次数
    repeat_times = int(max_ratio)
    remainder = max_ratio - repeat_times
    # 添加整数部分的重复次数
    new_lines.extend([line] * repeat_times)
    # 根据小数部分的概率决定是否再添加一次
    if random.random() < remainder:
        new_lines.append(line)

# 写入新的训练集文件
with open(new_train_file, 'w') as f:
    f.writelines(new_lines)
