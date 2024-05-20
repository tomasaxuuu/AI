from PIL import Image, ImageDraw
import numpy as np

# Цвета для каждого класса CIFAR-10
class_colors = [
    (255, 0, 0),     # Airplane (Red)
    (0, 255, 0),     # Automobile (Green)
    (0, 0, 255),     # Bird (Blue)
    (255, 255, 0),   # Cat (Yellow)
    (255, 0, 255),   # Deer (Magenta)
    (0, 255, 255),   # Dog (Cyan)
    (128, 0, 0),     # Frog (Maroon)
    (128, 128, 0),   # Horse (Olive)
    (0, 128, 0),     # Ship (Green)
    (0, 0, 128)      # Truck (Navy)
]

def create_class_image(class_index, image_path):
    # Создаем пустое изображение размером 32x32 пикселя
    img = Image.new('RGB', (32, 32), color=class_colors[class_index])

    # Сохраняем изображение
    img.save(image_path)

# Пример создания изображения для класса "Airplane"
create_class_image(0, './img/cifar10_airplane.png')
