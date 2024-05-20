import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt

# Список с названиями классов CIFAR-10
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

# Функция для предсказания класса изображения
def predict_image(model, image_path):
    # Загрузка и подготовка изображения
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Unable to load image at {image_path}")
        return None
    img = cv2.resize(img, (32, 32))
    img = img.reshape(1, 32, 32, 3).astype('float32') / 255

    # Визуализация изображения
    plt.imshow(img[0])
    plt.title("Input Image")
    plt.show()

    # Предсказание
    prediction = model.predict(img)
    class_index = np.argmax(prediction)
    class_name = class_names[class_index]
    print(f"Prediction probabilities: {prediction}")
    return class_name

# Основная программа
def main():
    # Загрузка данных CIFAR-10
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()

    # Подготовка данных
    x_test = x_test.astype('float32') / 255
    y_test = to_categorical(y_test, 10)

    # Загрузка модели
    model = load_model('cifar10_cnn_model.h5')

    # Оценка модели
    loss, accuracy = model.evaluate(x_test, y_test)
    print(f'Accuracy: {accuracy * 100:.2f}%')

    # Предсказание на новом изображении
    image_path = './img/frog.jpg'  # Укажите путь к вашему изображению лягушки
    predicted_class = predict_image(model, image_path)
    if predicted_class is not None:
        print(f'Predicted class: {predicted_class}')

if __name__ == "__main__":
    main()
