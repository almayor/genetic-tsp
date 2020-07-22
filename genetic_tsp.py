import numpy as np
import random
import matplotlib.pyplot as plt


class City:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, city):
        x_dist = abs(self.x - city.x)
        y_dist = abs(self.y - city.y)
        distance = np.sqrt(x_dist ** 2 + y_dist ** 2)
        return distance


class Route:

    def __init__(self, cities):
        self.cities = cities
        self.distance = self._calculate_distance()
        self.fitness = 1 / self.distance

    def _calculate_distance(self):
        self.distance = 0
        for i, from_city in enumerate(self.cities):
            to_city = self.cities[(i + 1) % len(self.cities)]
            self.distance += from_city.distance_to(to_city)

        return self.distance

    def mate_with(self, route):
        child_cities = list()

        # from parent 1
        start = random.randint(0, len(self.cities) - 1)
        end = random.randint(start, len(self.cities) - 1)
        child_cities = self.cities[start:end]

        # from parent 2
        for city in route.cities:
            if city not in child_cities:
                child_cities.append(city)

        return Route(child_cities)

    def mutate(self, mutation_rate):
        for i, _ in enumerate(self.cities):
            if random.random() < mutation_rate:
                j = random.randint(0, len(self.cities) - 1)
                self.cities[i], self.cities[j] = self.cities[j], self.cities[i]
    
    def plot(self, save=None):
        fig, ax = plt.subplots(figsize=(5, 5))
        xx = [city.x for city in self.cities] + [self.cities[0].x]
        yy = [city.y for city in self.cities] + [self.cities[0].y]
        ax.plot(xx, yy)
        plt.axis('off')
        if save:
            plt.savefig(save, dpi=500)


class Population:

    def __init__(self, cities, size):
        self.routes = list()
        self.size = size

        for _ in range(size):
            shuffled_cities = random.sample(cities, len(cities))
            self.routes.append(Route(shuffled_cities))

        self.routes = sorted(self.routes, key=lambda r: r.fitness, reverse=True)

    def best_route(self):
        return self.routes[0]

    def propagate(self, elite_size, mutation_rate):
        elite = self.routes[:elite_size]
        self.routes = elite
        while len(self.routes) < self.size:
            parent1, parent2 = random.sample(elite, 2)
            self.routes.append(parent1.mate_with(parent2))
        for route in self.routes:
            route.mutate(mutation_rate)
        self.routes = sorted(self.routes, key=lambda r: r.fitness, reverse=True)


if __name__ == "__main__":
    cities = list()
    for _ in range(50):
        cities.append(City(x=random.randint(0, 200), y=random.randint(0, 200)))

    popul = Population(cities, size=1000)
    best_distance = list()
    for i in range(500):
        popul.propagate(elite_size=400, mutation_rate=0.001)
        best_route = popul.best_route()
        print(best_route.distance)
        best_distance.append(best_route.distance)
#         best_route.plot(save=f"snapshots/generation_{i}.png")

#     fix, ax = plt.subplots(figsize=(7, 7))
#     ax.plot(range(len(best_distance)), best_distance, c='k')
#     plt.xlabel("Generation", fontsize=15)
#     plt.ylabel("Distance", fontsize=15)
#     ax.tick_params(axis="both", labelsize=12)
#     plt.title("Genetic algorithm on a 50-city TSP", fontsize=15)
#     plt.savefig("50_distance_generation.png", dpi=500)
