# 2025.6.27
# E:\remote\Yolo\arthroscopy_dataset\unzipped下面有很多名字类似1-002，1-003的文件夹，每个文件夹下有images和labels两个子文件夹，images/train路径下有png文件，labels/trai路径下有对应的用于yolo分割的txt文件，将无对应txt文件的png图片以1/3的概率保存到E:\remote\Yolo\arthroscopy_dataset\images\train_bg中以1750.png开始命名

import os
import random
import shutil

# 源文件夹根路径
source_root = r"E:\remote\Yolo\arthroscopy_dataset\unzipped"
# 目标文件夹路径
target_folder = r"E:\remote\Yolo\arthroscopy_dataset\images\train_bg"
# 确保目标文件夹存在
os.makedirs(target_folder, exist_ok=True)

# 初始化起始文件名编号
start_index = 1750

# 遍历源根路径下的所有子文件夹
for sub_folder in os.listdir(source_root):
    sub_folder_path = os.path.join(source_root, sub_folder)
    if os.path.isdir(sub_folder_path):
        # 构建 images/train 和 labels/train 路径
        images_train_path = os.path.join(sub_folder_path, "images", "train")
        labels_train_path = os.path.join(sub_folder_path, "labels", "train")

        # 检查路径是否存在
        if os.path.exists(images_train_path) and os.path.exists(labels_train_path):
            # 遍历 images/train 下的所有 PNG 文件
            for img_file in os.listdir(images_train_path):
                if img_file.lower().endswith('.png'):
                    # 构建对应的 txt 文件路径
                    txt_file_name = img_file.replace('.png', '.txt')
                    txt_file_path = os.path.join(labels_train_path, txt_file_name)

                    # 检查是否存在对应的 txt 文件
                    if not os.path.exists(txt_file_path):
                        # 以 1/3 的概率保存图片
                        if random.random() < 1/3:
                            source_img_path = os.path.join(images_train_path, img_file)
                            target_img_path = os.path.join(target_folder, f"{start_index}.png")
                            shutil.copyfile(source_img_path, target_img_path)
                            print(f"已复制图片 {source_img_path} 到 {target_img_path}")
                            start_index += 1
