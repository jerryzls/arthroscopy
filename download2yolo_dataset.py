# 2025.6.24
"""
  路径base_folder下有1-002~9-005文件夹，名字中间都是以‘-’连接，每个文件夹下有images和labels两个子文件夹，labels文件夹下有train子文件夹，train文件夹中有名字形如Image0002.txt的文件
  若该txt文件中第一个数字（一位数或者两位数）为[2,3,6,7]，则将该文件
  以0.7的概率保存到E:\remote\Yolo\arthroscopy_dataset\labels下的train文件夹中并命名为{i}.txt（i为第几个保存到该文件夹的txt文件），
  以0.2的概率保存到E:\remote\Yolo\arthroscopy_dataset\labels下的val文件夹中并命名为{j}.txt，
  以0.1的概率保存到E:\remote\Yolo\arthroscopy_dataset\labels下的test文件夹中并命名为{k}.txt，
  并将txt的第一个数字分别变为[0,1,2,3]。
  同时，该txt文件在原始labels文件夹所对应的images文件夹中的png图片同时保存到base_folder路径下对应的train，val或test文件中，命名为{i}.png，{j}.png或{k}.png
"""

import os
import random
import shutil

base_folder = r'E:\remote\Yolo\arthroscopy_dataset'
target_labels_base = os.path.join(base_folder, 'labels')
target_images_base = os.path.join(base_folder, 'images')

# 创建目标文件夹
train_labels_folder = os.path.join(target_labels_base, 'train')
val_labels_folder = os.path.join(target_labels_base, 'val')
test_labels_folder = os.path.join(target_labels_base, 'test')
train_images_folder = os.path.join(target_images_base, 'train')
val_images_folder = os.path.join(target_images_base, 'val')
test_images_folder = os.path.join(target_images_base, 'test')

for folder in [train_labels_folder, val_labels_folder, test_labels_folder, train_images_folder, val_images_folder, test_images_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# 初始化计数器
train_count = 0
val_count = 0
test_count = 0

# 遍历 1-002 到 9-005 文件夹
for i in range(1, 10):   # 根据情况改
    for j in range(1, 10):  # 根据情况改
        folder_name = f"{i}-00{j}"
        folder_path = os.path.join(base_folder, folder_name)
        if not os.path.exists(folder_path):
            continue

        labels_train_folder = os.path.join(folder_path, 'labels', 'train')
        images_folder = os.path.join(folder_path, 'images', 'train')

        if not os.path.exists(labels_train_folder):
            continue

        # 遍历 labels 文件夹下的 train 文件夹中的 txt 文件
        for txt_file in os.listdir(labels_train_folder):
            if txt_file.endswith('.txt'):
                txt_file_path = os.path.join(labels_train_folder, txt_file)
                with open(txt_file_path, 'r') as f:
                    first_line = f.readline().strip()
                    if first_line:
                        first_num = int(first_line.split()[0])
                        if first_num in [2, 3, 6, 7]:
                            # 映射第一个数字
                            new_first_num = [0, 1, 2, 3][[2, 3, 6, 7].index(first_num)]

                            # 根据概率分配文件
                            rand_num = random.random()
                            if rand_num < 0.7:
                                target_labels_folder = train_labels_folder
                                target_images_folder = train_images_folder
                                count = train_count
                                train_count += 1
                            elif rand_num < 0.9:
                                target_labels_folder = val_labels_folder
                                target_images_folder = val_images_folder
                                count = val_count
                                val_count += 1
                            else:
                                target_labels_folder = test_labels_folder
                                target_images_folder = test_images_folder
                                count = test_count
                                test_count += 1

                            # 保存修改后的 txt 文件
                            new_txt_path = os.path.join(target_labels_folder, f"{count}.txt")
                            with open(txt_file_path, 'r') as original_f, open(new_txt_path, 'w') as new_f:
                                lines = original_f.readlines()
                                if lines:
                                    parts = lines[0].split()
                                    parts[0] = str(new_first_num)
                                    new_f.write(' '.join(parts) + '\n')
                                    for line in lines[1:]:
                                        new_f.write(line)

                            # 保存对应的图片
                            image_name = txt_file.replace('.txt', '.png')
                            image_path = os.path.join(images_folder, image_name)
                            if os.path.exists(image_path):
                                new_image_path = os.path.join(target_images_folder, f"{count}.png")
                                shutil.copyfile(image_path, new_image_path)
                            else:
                                print(f"找不到对应的图片: {image_path}")

print("处理完成")
