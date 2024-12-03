import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from neo4j import GraphDatabase


class FertilizerSystem:
    def __init__(self, neo4j_uri, user, password):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(user, password))
        self.create_fuzzy_system()

    def create_fuzzy_system(self):

        self.soil = ctrl.Antecedent(np.arange(0, 11, 1), 'soil')
        self.weather = ctrl.Antecedent(np.arange(0, 11, 1), 'weather')
        self.plant = ctrl.Antecedent(np.arange(0, 11, 1), 'plant')


        self.dosage = ctrl.Consequent(np.arange(0, 151, 1), 'dosage')

        # Фаззификация
        self.soil['sandy'] = fuzz.trimf(self.soil.universe, [0, 0, 5])
        self.soil['clay'] = fuzz.trimf(self.soil.universe, [5, 10, 10])
        self.soil['medium'] = fuzz.trimf(self.soil.universe, [2, 5, 8])

        self.weather['rainy'] = fuzz.trimf(self.weather.universe, [0, 0, 5])
        self.weather['sunny'] = fuzz.trimf(self.weather.universe, [5, 10, 10])
        self.weather['cloudy'] = fuzz.trimf(self.weather.universe, [2, 5, 8])

        self.plant['wheat'] = fuzz.trimf(self.plant.universe, [0, 0, 5])
        self.plant['corn'] = fuzz.trimf(self.plant.universe, [5, 10, 10])

        self.dosage['low'] = fuzz.trimf(self.dosage.universe, [0, 0, 50])
        self.dosage['medium'] = fuzz.trimf(self.dosage.universe, [50, 75, 100])
        self.dosage['high'] = fuzz.trimf(self.dosage.universe, [100, 150, 150])

        # Правила
        rule1 = ctrl.Rule(self.soil['sandy'] & self.weather['rainy'], self.dosage['low'])
        rule2 = ctrl.Rule(self.soil['clay'] & self.weather['sunny'], self.dosage['high'])
        rule3 = ctrl.Rule(self.plant['corn'] & self.weather['cloudy'], self.dosage['medium'])
        rule4 = ctrl.Rule(self.soil['clay'] & self.weather['cloudy'], self.dosage['low'])

        # Универсальное правило (по умолчанию)
        rule_default = ctrl.Rule(self.soil['sandy'] | self.soil['clay'], self.dosage['medium'])

        # Управляющая система
        self.system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule_default])
        self.simulator = ctrl.ControlSystemSimulation(self.system)

    def create_sample_data(self):
        """
        Создание данных в базе Neo4j.
        """
        with self.driver.session() as session:
            session.run("""
            CREATE (a:Soil {type: 'Sandy', ph: 6.5})
            CREATE (b:Soil {type: 'Clay', ph: 7.0})
            CREATE (c:Plant {name: 'Wheat'})
            CREATE (d:Plant {name: 'Corn'})
            CREATE (a)-[:SUITABLE_FOR]->(c)
            CREATE (b)-[:SUITABLE_FOR]->(d)
            """)

    def fetch_data(self):

        with self.driver.session() as session:
            result = session.run("MATCH (n) RETURN n")
            for record in result:
                print(record)

    def get_recommendation(self, soil_type, plant_type, weather_condition):
        # Преобразование входных данных
        soil_map = {'Sandy': 2, 'Clay': 8}
        plant_map = {'Wheat': 2, 'Corn': 8}
        weather_map = {'Rainy': 2, 'Sunny': 8, 'Cloudy': 5}

        soil_value = soil_map.get(soil_type, 5)
        plant_value = plant_map.get(plant_type, 5)
        weather_value = weather_map.get(weather_condition, 5)

        # Проверка диапазонов
        if not (0 <= soil_value <= 10):
            raise ValueError(f"Soil value {soil_value} out of range (0-10)")
        if not (0 <= plant_value <= 10):
            raise ValueError(f"Plant value {plant_value} out of range (0-10)")
        if not (0 <= weather_value <= 10):
            raise ValueError(f"Weather value {weather_value} out of range (0-10)")

        print(f"Inputs: soil={soil_value}, plant={plant_value}, weather={weather_value}")

        # Установка значений
        self.simulator.input['soil'] = soil_value
        self.simulator.input['plant'] = plant_value
        self.simulator.input['weather'] = weather_value

        # Рассчёт
        try:
            self.simulator.compute()
            print(f"Simulator outputs: {self.simulator.output}")
        except Exception as e:
            print(f"Error during simulation: {e}")
            raise

        # Проверка результата
        if 'dosage' not in self.simulator.output:
            raise ValueError("Output variable 'dosage' not computed. Check rules or input values.")

        return self.simulator.output['dosage']

    def simulate(self):
        soils = ["Sandy", "Clay"]
        plants = ["Wheat", "Corn"]
        weathers = ["Rainy", "Sunny", "Cloudy"]

        for _ in range(5):
            soil = np.random.choice(soils)
            plant = np.random.choice(plants)
            weather = np.random.choice(weathers)
            try:
                dosage = self.get_recommendation(soil, plant, weather)
                print(f"Simulation: Soil={soil}, Plant={plant}, Weather={weather}, Dosage={dosage:.2f}")
            except ValueError as e:
                print(f"Simulation failed: {e}")

    def log_simulation_result(self, soil, plant, weather, dosage):

        with self.driver.session() as session:
            session.run("""
            CREATE (:SimulationResult {
                soil: $soil,
                plant: $plant,
                weather: $weather,
                dosage: $dosage
            })
            """, soil=soil, plant=plant, weather=weather, dosage=dosage)

    def simulate(self):
        """
        Запускает симуляцию и сохраняет результаты в Neo4j.
        """
        soils = ["Sandy", "Clay"]
        plants = ["Wheat", "Corn"]
        weathers = ["Rainy", "Sunny", "Cloudy"]

        for _ in range(5):
            soil = np.random.choice(soils)
            plant = np.random.choice(plants)
            weather = np.random.choice(weathers)
            try:
                dosage = self.get_recommendation(soil, plant, weather)
                print(f"Simulation: Soil={soil}, Plant={plant}, Weather={weather}, Dosage={dosage:.2f}")
                # Сохранение результата в базу
                self.log_simulation_result(soil, plant, weather, dosage)
            except ValueError as e:
                print(f"Simulation failed: {e}")


if __name__ == "__main__":
    # Инициализация системы
    neo4j_uri = "neo4j+s://5fd4a7dc.databases.neo4j.io"
    user = "neo4j"
    password = "9Df_QXvzK1JrFZpnHvww5P32fwa7qH7-kwWcIu8kx6g"

    system = FertilizerSystem(neo4j_uri, user, password)

    # Создание данных в базе
    print("Creating sample data in Neo4j...")
    system.create_sample_data()

    # Проверка созданных данных
    print("Fetching data from Neo4j...")
    system.fetch_data()

    # Запуск симуляции
    print("Running simulation...")
    system.simulate()
