# 2025.6.26
# 路径E:\remote\Yolo\arthroscopy_dataset\2-006old下有images和labels两个文件夹，labels文件夹下有名字形如Image0002.txt的文件
# 若该txt文件中每行第一个数字（一位数或者两位数）为[2,3,6,7]中一个，则将该文件（第一个数字不是[2,3,6,7]中一个的行不保存）保存到E:\remote\Yolo\arthroscopy_dataset\labels下的2-006文件夹中并命名为{i}.txt，
# 并将txt的那行第一个数字对应变为[0,1,2,3]。
# 同时，该txt文件在原始labels文件夹所对应的images文件夹中的png图片同时保存到E:\remote\Yolo\arthroscopy_dataset\images路径下对应的2-006文件中，命名为{i}.png

import os
import shutil

# 定义原始路径和目标路径
old_base_path = r"E:\remote\Yolo\arthroscopy_dataset\2-006old"
old_labels_path = os.path.join(old_base_path, "labels")
old_images_path = os.path.join(old_base_path, "images")

new_base_path = r"E:\remote\Yolo\arthroscopy_dataset"
new_labels_path = os.path.join(new_base_path, "labels", "2-006")
new_images_path = os.path.join(new_base_path, "images", "2-006")

# 创建目标文件夹
os.makedirs(new_labels_path, exist_ok=True)
os.makedirs(new_images_path, exist_ok=True)

# 定义原始类别和新类别映射
old_classes = [2, 3, 6, 7]
new_classes = [0, 1, 2, 3]
class_mapping = dict(zip(old_classes, new_classes))

i = 0
# 遍历原始 labels 文件夹下的所有 txt 文件
for txt_file in os.listdir(old_labels_path):
    if txt_file.endswith('.txt'):
        old_txt_path = os.path.join(old_labels_path, txt_file)
        new_lines = []
        # 读取 txt 文件
        with open(old_txt_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if parts:
                    try:
                        class_id = int(parts[0])
                        if class_id in old_classes:
                            new_class_id = class_mapping[class_id]
                            parts[0] = str(new_class_id)
                            new_lines.append(" ".join(parts) + "\n")
                    except ValueError:
                        continue

        # 如果有符合条件的行，保存新的 txt 文件
        if new_lines:
            new_txt_path = os.path.join(new_labels_path, f"{i}.txt")
            with open(new_txt_path, 'w') as f:
                f.writelines(new_lines)

            # 复制对应的 png 图片
            img_name = txt_file.replace('.txt', '.png')
            old_img_path = os.path.join(old_images_path, img_name)
            if os.path.exists(old_img_path):
                new_img_path = os.path.join(new_images_path, f"{i}.png")
                shutil.copyfile(old_img_path, new_img_path)

            i += 1
