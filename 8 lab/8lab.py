import numpy as np
import matplotlib.pyplot as plt

# Треугольная функция принадлежности
def triangular_mf(x, a, b, c):
    """
    Треугольная функция принадлежности.
    :param x: Точки, для которых вычисляется функция принадлежности.
    :param a: Левая граница начала возрастания функции.
    :param b: Вершина треугольника, где принадлежность равна 1.
    :param c: Правая граница окончания убывания функции.
    :return: Значение функции принадлежности в точках x.
    """
    return np.maximum(0, np.minimum((x - a) / (b - a + 1e-6), (c - x) / (c - b + 1e-6)))

# Операция импликации (минимум)
def fuzzy_implication(set1, set2):
    return np.minimum(set1, set2)

# Универсум для уровня заряда и скорости
x_battery = np.linspace(0, 100, 500)  # Уровень заряда батареи от 0% до 100%
x_speed = np.linspace(0, 100, 500)    # Скорость движения от 0% до 100%

# Определение функций принадлежности для уровня заряда батареи
low_battery = triangular_mf(x_battery, 0, 20, 40)    # Низкий заряд: максимум до 20-40%
medium_battery = triangular_mf(x_battery, 30, 50, 70) # Средний заряд: максимум в 50%
high_battery = triangular_mf(x_battery, 60, 80, 100)  # Высокий заряд: максимум 80-100%

# Определение функций принадлежности для скорости движения
slow_speed = triangular_mf(x_speed, 0, 20, 40)        # Медленная скорость: максимум до 20-40%
medium_speed = triangular_mf(x_speed, 30, 50, 70)     # Средняя скорость: максимум в 50%
fast_speed = triangular_mf(x_speed, 60, 80, 100)      # Быстрая скорость: максимум 80-100%

# Ввод данных пользователем
battery_value = float(input("Введите уровень заряда батареи (0-100): "))
speed_value = float(input("Введите скорость движения (0-100): "))

# Найдем значения функций принадлежности для заданного уровня заряда батареи и скорости
battery_mf = {
    "low_battery": np.interp(battery_value, x_battery, low_battery),
    "medium_battery": np.interp(battery_value, x_battery, medium_battery),
    "high_battery": np.interp(battery_value, x_battery, high_battery),
}

speed_mf = {
    "slow_speed": np.interp(speed_value, x_speed, slow_speed),
    "medium_speed": np.interp(speed_value, x_speed, medium_speed),
    "fast_speed": np.interp(speed_value, x_speed, fast_speed),
}

# Вывод в консоль значений функций принадлежности
print(f"Уровень заряда {battery_value}%: Низкий = {battery_mf['low_battery']:.2f}, Средний = {battery_mf['medium_battery']:.2f}, Высокий = {battery_mf['high_battery']:.2f}")
print(f"Скорость {speed_value}%: Медленная = {speed_mf['slow_speed']:.2f}, Средняя = {speed_mf['medium_speed']:.2f}, Быстрая = {speed_mf['fast_speed']:.2f}")

# Применим правило: "Если низкий заряд, то медленная скорость"
implication_result = fuzzy_implication(low_battery, slow_speed)

# Визуализация и вывод данных с учетом введенных значений
def plot_fuzzy_sets_with_values(x, sets, labels, title, user_value, user_label, user_membership):
    plt.figure(figsize=(10, 6))
    for i, (s, label) in enumerate(zip(sets, labels)):
        plt.plot(x, s, label=label)
        print(f"\nЗначения для {label}:")
        for j in range(0, len(x), 100):  # Выводим каждые 100 шагов для наглядности
            print(f"x = {x[j]:.2f}, принадлежность = {s[j]:.4f}")
    # Добавим точку для пользовательского значения
    plt.scatter(user_value, user_membership, color='red', zorder=5, label=f'{user_label} = {user_value}%')
    plt.title(title)
    plt.xlabel("Значение (%)")
    plt.ylabel("Принадлежность")
    plt.legend()
    plt.grid(True)
    plt.show()

# Визуализация нечетких множеств для уровня заряда батареи с введенным значением
plot_fuzzy_sets_with_values(x_battery, [low_battery, medium_battery, high_battery],
                            ["Низкий заряд", "Средний заряд", "Высокий заряд"],
                            "Нечеткие множества для уровня заряда батареи",
                            battery_value, "Уровень заряда", max(battery_mf.values()))

# Визуализация нечетких множеств для скорости движения с введенным значением
plot_fuzzy_sets_with_values(x_speed, [slow_speed, medium_speed, fast_speed],
                            ["Медленная скорость", "Средняя скорость", "Быстрая скорость"],
                            "Нечеткие множества для скорости движения",
                            speed_value, "Скорость", max(speed_mf.values()))

# Визуализация результата импликации с введенным значением
plot_fuzzy_sets_with_values(x_battery, [implication_result],
                            ["Импликация (Если низкий заряд -> медленная скорость)"],
                            "Результат импликации",
                            battery_value, "Уровень заряда", np.interp(battery_value, x_battery, implication_result))
