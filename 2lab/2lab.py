import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


x1 = np.linspace(0, 1, 400)
x2 = np.linspace(0, 1, 400)
y = x1**6 + x2**2 + x1**3 + 4*x2 + 5

df = pd.DataFrame({'x1': x1, 'x2': x2, 'y': y})
df.to_csv('data.csv', index=False)
df = pd.read_csv('data.csv')

# График для y = c1 (константа)
plt.figure(figsize=(10, 6))
plt.scatter(df['x1'], df['y'], label='x1^6 + x2^2 + x1^3 + 4*x2 + 5')
plt.xlabel('x1')
plt.ylabel('y')
plt.legend()
plt.title('Диаграмма рассеяния для y = x1^6 + x2^2 + x1^3 + 4*x2 + 5')
plt.show()

# График для y = c2 (константа)
plt.figure(figsize=(10, 6))
plt.scatter(df['x2'], df['y'], label='y = x1^6 + x2^2 + x1^3 + 4*x2 + 5')
plt.xlabel('x2')
plt.ylabel('y')
plt.legend()
plt.title('Диаграмма рассеяния для y = x1^6 + x2^2 + x1^3 + 4*x2 + 5')
plt.show()

# Вывод информации

print(f'Статистика для столбца x1:\n'
      f'Среднее: {np.mean(df["x1"])}\n'
      f'Минимум: {np.min(df["x1"])}\n'
      f'Максимум: {np.max(df["x1"])}')

print(f'\nСтатистика для столбца x2:\n'
      f'Среднее: {np.mean(df["x2"])}\n'
      f'Минимум: {np.min(df["x2"])}\n'
      f'Максимум: {np.max(df["x2"])}\n')

print(f'\nСтатистика для столбца y:\n'
      f'Среднее: {np.mean(df["y"])}\n'
      f'Минимум: {np.min(df["y"])}\n'
      f'Максимум: {np.max(df["y"])}')


# Сохранение строк в новый CSV файл
filtered_df = df[(df['x1'] < np.mean(df['x1'])) | (df['x2'] < np.mean(df['x2']))]
filtered_df.to_csv('filtered_data.csv', index=False)

# 3D график
x1, x2 = np.meshgrid(x1, x2)
Y = np.array(y).reshape((400, 1))
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x1, x2, Y, cmap='plasma')
ax.set_title('x1^6 + x2^2 + x1^3 + 4*x2 + 5')
plt.show()