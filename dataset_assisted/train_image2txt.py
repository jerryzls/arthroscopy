# 2025.6.25
# 把train_image_dir路径下的png用于训练的图片变为train.txt文件
# 根据需要修改stage、train_image_dir和train_txt_path

import os

stage = 'train'

# 训练图像所在目录
train_image_dir = fr"E:\remote\Yolo\arthroscopy_dataset\images\{stage}"
# 要生成的 train.txt 文件路径
train_txt_path = fr"E:\remote\Yolo\arthroscopy_dataset\images\{stage}.txt"

# 支持的图像文件扩展名
image_extensions = ('.jpg', '.jpeg', '.png', '.bmp')

# 获取目录下所有支持格式的图像文件路径
image_files = [f for f in os.listdir(train_image_dir) if f.lower().endswith(image_extensions)]

# 将相对路径写入 train.txt 文件
with open(train_txt_path, 'w', encoding='utf-8') as f:
    for img_name in image_files:
        relative_path = os.path.join("arthroscopy", "images", stage, img_name).replace('\\', '/')
        f.write(f"{relative_path}\n")

print(f"已将 {len(image_files)} 个图像路径写入 {train_txt_path}")
