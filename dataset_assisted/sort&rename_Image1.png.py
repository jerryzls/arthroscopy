# 2025.7.5
# 对指定目录source_folder下的文件ImageX.png按特定规则排序，再将这些文件重命名为 ImageXXXX.png 格式，其中 XXXX 是从 0001 开始递增的序号。

import os

def extract_number(filename):
    try:
        # 查找 'Image' 字符串并提取后面的数字部分
        start = filename.index('Image') + len('Image')
        end = filename.index('.', start)
        return int(filename[start:end])
    except (ValueError, IndexError):
        # 若提取失败，返回一个很大的整数，确保排在后面
        return 999999999

# 源文件路径
source_folder = r'\\yigongzuNAS\ZhuLingSong\PureVue_Camera\3\video_frame\Patient_001 00_00_04-00_01_54'

# 检查路径是否存在
if not os.path.exists(source_folder):
    print(f"指定路径 {source_folder} 不存在。")
else:
    # 获取指定路径下的所有文件
    files = os.listdir(source_folder)
    # 按 Image 后的数字排序，若没有则排在后面
    files.sort(key=extract_number)

    # 初始化序号
    i = 1

    for file in files:
        file_path = os.path.join(source_folder, file)
        if os.path.isfile(file_path):
            # 构建新的文件名
            new_file_name = f"Image{i:04d}.png"
            new_file_path = os.path.join(source_folder, new_file_name)
            try:
                # 重命名文件
                os.rename(file_path, new_file_path)
                print(f"已将 {file} 重命名为 {new_file_name}")
            except Exception as e:
                print(f"重命名 {file} 时出错: {e}")
            i += 1
