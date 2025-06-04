from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c  # in kilometers

def build_distance_matrix(places):
    n = len(places)
    matrix = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = haversine(
                    places[i].lat, places[i].lon,
                    places[j].lat, places[j].lon
                )
            # Optional: matrix[i][i] stays 0
    return matrix

if __name__ == "__main__":
    from utils import load_places

    places = load_places()
    matrix = build_distance_matrix(places)

    # Print matrix
    for row in matrix:
        print(["{:.2f}".format(dist) for dist in row])

