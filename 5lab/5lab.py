import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AffinityPropagation, MeanShift
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score

# Загрузка данных
file_path = './OrdonezA_ADLs_1.data'
df = pd.read_csv(file_path, header=None)

# Масштабирование признаков
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df.iloc[:, :-1])  # Масштабируем все столбцы кроме последнего (целевой класс)


# Метод локтя для определения оптимального числа кластеров
def plot_elbow_method(scaled_features):
    distortions = []
    K = range(1, 21)
    for k in K:
        kmean_model = KMeans(n_clusters=k, random_state=42)
        kmean_model.fit(scaled_features)
        distortions.append(kmean_model.inertia_)

    plt.figure(figsize=(12, 6))
    plt.plot(K, distortions, 'bx-')
    plt.xlabel('Количество кластеров')
    plt.ylabel('Искажение')
    plt.title('Метод локтя для оптимального числа кластеров')
    plt.show()


plot_elbow_method(scaled_features)

# Применение алгоритмов кластеризации
algorithms = {
    "KMeans": KMeans(n_clusters=15, random_state=42),  # Указываем 15 кластеров согласно числу классов в данных
    "Affinity Propagation": AffinityPropagation(),
    "Mean Shift": MeanShift()
}

results = []

# Обучение и оценка алгоритмов
for name, algorithm in algorithms.items():
    model = algorithm.fit(scaled_features)
    labels = model.labels_
    silhouette_avg = silhouette_score(scaled_features, labels)
    calinski_harabasz = calinski_harabasz_score(scaled_features, labels)
    davies_bouldin = davies_bouldin_score(scaled_features, labels)

    results.append((name, silhouette_avg, calinski_harabasz, davies_bouldin))
    print(f"{name}:")
    print(f"  Silhouette Score = {silhouette_avg:.4f}")
    print(f"  Calinski-Harabasz Index = {calinski_harabasz:.4f}")
    print(f"  Davies-Bouldin Index = {davies_bouldin:.4f}")

    # Визуализация кластеров (используем первые два признака для 2D визуализации)
    plt.figure(figsize=(12, 6))
    plt.scatter(scaled_features[:, 0], scaled_features[:, 1], c=labels, cmap='viridis')
    plt.title(f"{name} Clustering")
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.colorbar(label='Cluster')
    plt.show()

# Определение наилучшего алгоритма по silhouette score
best_algorithm = max(results, key=lambda x: x[1])
print(f"\nНаилучший алгоритм по Silhouette Score: {best_algorithm[0]} с Silhouette Score = {best_algorithm[1]:.4f}")

# Определение наилучшего алгоритма по Calinski-Harabasz Index
best_algorithm_ch = max(results, key=lambda x: x[2])
print(
    f"Наилучший алгоритм по Calinski-Harabasz Index: {best_algorithm_ch[0]} с Calinski-Harabasz Index = {best_algorithm_ch[2]:.4f}")

# Определение наилучшего алгоритма по Davies-Bouldin Index
best_algorithm_db = min(results, key=lambda x: x[3])
print(
    f"Наилучший алгоритм по Davies-Bouldin Index: {best_algorithm_db[0]} с Davies-Bouldin Index = {best_algorithm_db[3]:.4f}")