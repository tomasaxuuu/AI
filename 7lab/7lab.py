import random
import itertools
import matplotlib.pyplot as plt

# Пример данных о продуктах
products = [
    {"name": "Apple", "calories": 52, "proteins": 0.3, "fats": 0.2, "carbs": 14, "price": 10},
    {"name": "Banana", "calories": 96, "proteins": 1.3, "fats": 0.3, "carbs": 27, "price": 15},
    {"name": "Chicken Breast", "calories": 165, "proteins": 31, "fats": 3.6, "carbs": 0, "price": 180},
    {"name": "Rice", "calories": 130, "proteins": 2.7, "fats": 0.3, "carbs": 28, "price": 30},
    {"name": "Salmon", "calories": 208, "proteins": 20, "fats": 13, "carbs": 0, "price": 120},
    {"name": "Eggs", "calories": 155, "proteins": 13, "fats": 11, "carbs": 1.1, "price": 25},
    {"name": "Milk", "calories": 42, "proteins": 3.4, "fats": 1, "carbs": 5, "price": 20},
    {"name": "Broccoli", "calories": 55, "proteins": 3.7, "fats": 0.6, "carbs": 11, "price": 12},
    {"name": "Almonds", "calories": 579, "proteins": 21, "fats": 50, "carbs": 22, "price": 150},
    {"name": "Avocado", "calories": 160, "proteins": 2, "fats": 15, "carbs": 9, "price": 50},
    {"name": "Cheese", "calories": 402, "proteins": 25, "fats": 33, "carbs": 1.3, "price": 90},
    {"name": "Bread", "calories": 265, "proteins": 9, "fats": 3.2, "carbs": 49, "price": 18},
    {"name": "Pasta", "calories": 157, "proteins": 6, "fats": 1.1, "carbs": 30, "price": 25}
]

# Параметры задачи
norm = {"calories": 2000, "proteins": 100, "fats": 50, "carbs": 300}
price_limit = 500
k = 4  # количество продуктов в рационе


# Функция приспособленности (fitness)
def fitness(diet):
    total = {"calories": 0, "proteins": 0, "fats": 0, "carbs": 0, "price": 0}
    for product in diet:
        total["calories"] += product["calories"]
        total["proteins"] += product["proteins"]
        total["fats"] += product["fats"]
        total["carbs"] += product["carbs"]
        total["price"] += product["price"]

    if total["price"] > price_limit:
        return float('inf')  # если бюджет превышен, решение не годится

    # Отклонение от нормы по характеристикам
    deviation = (
            abs(total["calories"] - norm["calories"]) +
            abs(total["proteins"] - norm["proteins"]) +
            abs(total["fats"] - norm["fats"]) +
            abs(total["carbs"] - norm["carbs"])
    )

    # Функция приспособленности учитывает как отклонение, так и цену
    return deviation + total["price"] / 10  # Цена учитывается как малый штраф


# Турнирная селекция
def tournament_selection(population, tournament_size=5):
    selected = random.sample(population, tournament_size)
    selected = sorted(selected, key=fitness)
    return selected[0]


# Скрещивание (разные типы)
def crossover(parent1, parent2, method='single'):
    if method == 'single':
        point = random.randint(1, k - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
    elif method == 'two_point':
        point1 = random.randint(1, k - 2)
        point2 = random.randint(point1, k - 1)
        child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
    elif method == 'uniform':
        # Равномерное скрещивание
        child1, child2 = [], []
        for i in range(k):
            if random.random() < 0.5:
                child1.append(parent1[i])
                child2.append(parent2[i])
            else:
                child1.append(parent2[i])
                child2.append(parent1[i])
    return child1, child2


# Мутация (разные типы)
def mutation(diet, method='swap'):
    if method == 'swap':
        index = random.randint(0, k - 1)
        diet[index] = random.choice(products)
    elif method == 'inverse':
        index1, index2 = sorted(random.sample(range(k), 2))
        diet[index1:index2] = reversed(diet[index1:index2])
    elif method == 'shuffle':
        # Случайная перестановка элементов
        random.shuffle(diet)
    return diet


# Генетический алгоритм с турнирной селекцией и усиленными мутациями
def genetic_algorithm(cross_method, mut_method, pop_size=100, generations_count=100):
    # Инициализация популяции с увеличенным разнообразием
    population = [random.sample(products, k) for _ in range(pop_size)]

    generations = []
    best_fitness_values = []

    # Эволюционный процесс
    for generation in range(generations_count):
        # Оценка популяции
        population = sorted(population, key=fitness)

        # Сохранение лучшего значения приспособленности
        best_fitness = fitness(population[0])
        generations.append(generation)
        best_fitness_values.append(best_fitness)

        # Новая популяция через турнирную селекцию, скрещивание и мутацию
        new_population = []
        for _ in range(pop_size // 2):  # создаем новых потомков
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child1, child2 = crossover(parent1, parent2, method=cross_method)
            new_population.append(mutation(child1, method=mut_method))
            new_population.append(mutation(child2, method=mut_method))

        population = new_population  # обновляем популяцию

    return population[0], generations, best_fitness_values


# Функция для вывода общих характеристик рациона
def print_diet_info(diet):
    total = {"calories": 0, "proteins": 0, "fats": 0, "carbs": 0, "price": 0}
    for product in diet:
        total["calories"] += product["calories"]
        total["proteins"] += product["proteins"]
        total["fats"] += product["fats"]
        total["carbs"] += product["carbs"]
        total["price"] += product["price"]
    print(f"Общие характеристики рациона:\n"
          f"Цена: {total['price']} рублей\n"
          f"Калории: {total['calories']} ккал\n"
          f"Белки: {total['proteins']} г\n"
          f"Жиры: {total['fats']} г\n"
          f"Углеводы: {total['carbs']} г")


# Основная часть, где тестируем все комбинации и рисуем графики
cross_methods = ['single', 'two_point', 'uniform']
mut_methods = ['swap', 'inverse', 'shuffle']

plt.figure(figsize=(10, 7))

# Проходим по каждой комбинации методов скрещивания и мутации
for cross_method in cross_methods:
    for mut_method in mut_methods:
        best_diet, generations, best_fitness_values = genetic_algorithm(cross_method, mut_method, pop_size=100,
                                                                        generations_count=50)
        plt.plot(generations, best_fitness_values, label=f"{cross_method} + {mut_method}")

        # Вывод лучших рационов и общих характеристик
        print(f"\nМетод скрещивания: {cross_method}, метод мутации: {mut_method}")
        print("Лучший рацион:")
        for product in best_diet:
            print(
                f"{product['name']}: Калории: {product['calories']}, Белки: {product['proteins']}, Жиры: {product['fats']}, Углеводы: {product['carbs']}, Цена: {product['price']}"
            )

        # Вывод общих характеристик лучшего рациона
        print_diet_info(best_diet)

# Настройки графика
plt.xlabel("Поколение")
plt.ylabel("Приспособленность (отклонение от нормы + цена)")
plt.title("Изменение фитнеса в поколениях для различных методов скрещивания и мутации")
plt.legend()
plt.show()