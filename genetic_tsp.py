import matplotlib.pyplot as plt
import numpy as np
import os
import random


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
    
    def plot(self, save=None):
        fig, ax = plt.subplots(figsize=(5, 5))
        xx = [city.x for city in self.cities] + [self.cities[0].x]
        yy = [city.y for city in self.cities] + [self.cities[0].y]
        ax.plot(xx, yy, c='k')
        ax.scatter(xx, yy, c='r')
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

    def propagate(self, elite_size):
        elite = self.routes[:elite_size]
        self.routes = elite
        while len(self.routes) < self.size:
            parent1, parent2 = random.sample(elite, 2)
            self.routes.append(parent1.mate_with(parent2))
        self.routes = sorted(self.routes, key=lambda r: r.fitness, reverse=True)


def run_algorithm(n_cities, n_generations, snap_freq):
    if not os.path.exists(f"snapshots_{n_cities}cities"):
        os.mkdir(f"snapshots_{n_cities}cities")

    cities = list()
    for _ in range(n_cities):
        cities.append(City(x=random.randint(0, 200), y=random.randint(0, 200)))
    
    popul = Population(cities, size=1000)
    best_distance = list()
    for i in range(n_generations):
        popul.propagate(elite_size=300)
        best_route = popul.best_route()
        print(best_route.distance)
        best_distance.append(best_route.distance)
        if i % snap_freq == 0:
            best_route.plot(save=f"snapshots_{n_cities}cities/generation_{i}.png")
    
    fix, ax = plt.subplots(figsize=(7, 7))
    ax.plot(range(len(best_distance)), best_distance, c='k')
    plt.xlabel("Generation", fontsize=15)
    plt.ylabel("Distance", fontsize=15)
    ax.tick_params(axis="both", labelsize=12)
    plt.title(f"Genetic algorithm on a {n_cities}-city TSP", fontsize=15)
    plt.savefig(f"{n_cities}_distance_generation.png", dpi=500)
    
    
if __name__ == "__main__":
    run_algorithm(25, 200, 1)
    run_algorithm(50, 400, 10)
    run_algorithm(100, 2500, 10)
