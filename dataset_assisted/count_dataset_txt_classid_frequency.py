"""
2025.6.24
统计指定train_labels_folder文件夹下所有 txt 文件中每行第一个class id为 0、1、2、3 的出现次数
"""

import os

# 定义目标文件夹路径
train_labels_folder = r'E:\remote\Yolo\arthroscopy_dataset\labels\test'

# 初始化计数器
count_dict = {0: 0, 1: 0, 2: 0, 3: 0}
# count_dict = {2: 0, 3: 0, 6: 0, 7: 0}

# 遍历文件夹下所有 txt 文件
for filename in os.listdir(train_labels_folder):
    if filename.endswith('.txt'):
        file_path = os.path.join(train_labels_folder, filename)
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        first_num_str = line.split()[0]
                        if first_num_str.isdigit():
                            first_num = int(first_num_str)
                            if first_num in count_dict:
                                count_dict[first_num] += 1
        except Exception as e:
            print(f"读取文件 {file_path} 时出错: {e}")

# 输出统计结果
for num, count in count_dict.items():
    print(f"数字 {num} 的个数: {count}")
