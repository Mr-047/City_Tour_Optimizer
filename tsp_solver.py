from pathlib import Path

def greedy_tsp(start_idx, dist_matrix):
    n = len(dist_matrix)
    visited = [False] * n
    route = [start_idx]
    visited[start_idx] = True
    current = start_idx

    while len(route) < n:
        nearest = None
        min_dist = float('inf')

        for j in range(n):
            if not visited[j] and dist_matrix[current][j] < min_dist:
                nearest = j
                min_dist = dist_matrix[current][j]

        route.append(nearest)
        visited[nearest] = True
        current = nearest

def greedy_tsp(start_idx, dist_matrix):
    n = len(dist_matrix)
    visited = [False] * n
    route = [start_idx]
    visited[start_idx] = True
    current = start_idx

    while len(route) < n:
        nearest = None
        min_dist = float('inf')

        for j in range(n):
            if not visited[j] and dist_matrix[current][j] < min_dist:
                nearest = j
                min_dist = dist_matrix[current][j]

        route.append(nearest)
        visited[nearest] = True
        current = nearest

    return route

def two_opt(route, dist_matrix):
    best = route.copy()
    improved = True
    n = len(route)

    def route_distance(route):
        return sum(dist_matrix[route[i]][route[i + 1]] for i in range(len(route) - 1))

    while improved:
        improved = False
        best_distance = route_distance(best)

        for i in range(1, n - 2):
            for j in range(i + 1, n - 1):
                if j - i == 1:
                    continue  # adjacent nodes, skip

                new_route = best[:i] + best[i:j][::-1] + best[j:]
                new_distance = route_distance(new_route)

                if new_distance < best_distance:
                    best = new_route
                    improved = True
                    break  # improvement found, restart loop
            if improved:
                break

    return best

import math
import random

def simulated_annealing(route, dist, initial_temp=1000, cooling_rate=0.995, stopping_temp=1e-3):
    def swap(route):
        i, j = sorted(random.sample(range(1, len(route)-1), 2))
        new_route = route[:i] + route[i:j+1][::-1] + route[j+1:]
        return new_route

    def acceptance_probability(old_cost, new_cost, temperature):
        if new_cost < old_cost:
            return 1.0
        return math.exp((old_cost - new_cost) / temperature)

    current_route = route[:]
    best_route = route[:]
    current_cost = route_distance(route, dist)
    best_cost = current_cost
    temperature = initial_temp

    while temperature > stopping_temp:
        new_route = swap(current_route)
        new_cost = route_distance(new_route, dist)
        ap = acceptance_probability(current_cost, new_cost, temperature)

        if ap > random.random():
            current_route = new_route
            current_cost = new_cost

            if new_cost < best_cost:
                best_route = new_route
                best_cost = new_cost

        temperature *= cooling_rate

    return best_route


def route_distance(route, dist_matrix):
    return sum(dist_matrix[route[i]][route[i + 1]] for i in range(len(route) - 1))


if __name__ == "__main__":
    from utils import load_places
    from distance import build_distance_matrix

    places = load_places()
    dist = build_distance_matrix(places)

    start = 0
    greedy_route = greedy_tsp(start, dist)

    print("\nGreedy Route:")
    for idx in greedy_route:
        print(f"{idx}: {places[idx].name}")

    # Now improve the route using 2-opt
    optimized_route = two_opt(greedy_route, dist)

    print("\nOptimized Route (2-opt):")
    for idx in optimized_route:
        print(f"{idx}: {places[idx].name}")

