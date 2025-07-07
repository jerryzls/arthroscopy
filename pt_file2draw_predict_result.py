# 2025.7.7
# 使用YOLOv11训练出来的best.pt预测边界框

from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np

def add_custom_labels(image, results):
    # 将 OpenCV 的 BGR 图像转换为 PIL 的 RGB 图像
    img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    try:
        # 尝试加载指定字体
        font = ImageFont.truetype(r'E:\remote\Yolo\Arial.Unicode.ttf', 16)
    except Exception as e:
        print(f"加载字体失败: {e}，使用默认字体")
        font = ImageFont.load_default()

    for box in results.boxes:
        # 获取边界框坐标，转换为整数类型
        xyxy = box.xyxy[0].cpu().numpy().astype(int)
        # 检查坐标是否在图像尺寸范围内
        img_width, img_height = img.size
        xyxy[0] = max(0, xyxy[0])
        xyxy[1] = max(0, xyxy[1])
        xyxy[2] = min(img_width, xyxy[2])
        xyxy[3] = min(img_height, xyxy[3])

        # 获取类别索引
        cls = int(box.cls[0])
        # 获取置信度
        conf = box.conf[0].cpu().numpy()
        # 生成标签文本
        label = f"{results.names[cls]}: {conf:.2f}"

        # 绘制边界框
        draw.rectangle(tuple(xyxy), outline=(255, 0, 0), width=5)

        # 使用 textbbox 方法计算标签文本的尺寸
        bbox = draw.textbbox((0, 0), label, font=font)
        label_width = bbox[2] - bbox[0]
        label_height = bbox[3] - bbox[1]

        # 计算标签背景框的位置
        label_x = xyxy[0]
        label_y = xyxy[1] - label_height - 5 if xyxy[1] - label_height - 5 > 0 else xyxy[1] + 5
        # 绘制标签背景框
        draw.rectangle([(label_x, label_y), (label_x + label_width, label_y + label_height)], fill=(255, 0, 0))
        # 绘制标签文本
        draw.text((label_x, label_y), label, font=font, fill=(255, 255, 255))

    # 将 PIL 图像转换回 OpenCV 的 BGR 图像
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


if __name__ == '__main__':
    # 加载模型
    model = YOLO(model=r'E:\remote\Yolo\train_result\train_balanced_result\weights\best.pt')
    # 进行预测，不保存和显示结果
    results = model.predict(source=r"E:\remote\Yolo\arthroscopy_dataset\images\2-006\0.png", save=False, show=False)

    # 读取原始图像
    image = cv2.imread(r"E:\remote\Yolo\arthroscopy_dataset\images\2-006\0.png")
    # 添加自定义标签和方框
    image_with_labels = add_custom_labels(image, results[0])

    # 显示结果图像
    cv2.imshow('Result', image_with_labels)
    # 等待按键事件
    cv2.waitKey(0)
    # 关闭所有 OpenCV 窗口
    cv2.destroyAllWindows()

    # 如果检测到目标，保存结果图像
    if results[0].boxes:
        cv2.imwrite('result.png', image_with_labels)
