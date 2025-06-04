from collections import namedtuple
import csv
from pathlib import Path
from datetime import datetime

# Define the Place data model
Place = namedtuple("Place", ["name", "lat", "lon", "open_time", "close_time"])

# Dynamically construct the path to data/places.csv
BASE_DIR = Path(__file__).resolve().parent  # Gets the folder where utils.py is
DATA_PATH = BASE_DIR / "data" / "places.csv"

def load_places(csv_path=DATA_PATH):
    places = []

    with open(csv_path, "r", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["Name"].strip()
            lat = float(row["Lat"].strip())
            lon = float(row["Lon"].strip())
            open_time = datetime.strptime(row["OpenTime"].strip(), "%H:%M").time()
            close_time = datetime.strptime(row["CloseTime"].strip(), "%H:%M").time()
            places.append(Place(name, lat, lon, open_time, close_time))

    return places

import matplotlib.pyplot as plt

def plot_route(places, route, save_path="output/route_plot.png"):
    x = [places[i].lon for i in route]
    y = [places[i].lat for i in route]
    labels = [places[i].name for i in route]

    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color='red', zorder=5)

    # Draw arrows between points
    for i in range(len(route) - 1):
        plt.annotate("",
                     xy=(x[i+1], y[i+1]),
                     xytext=(x[i], y[i]),
                     arrowprops=dict(arrowstyle="->", color="blue", lw=1),
                     zorder=4)

    # Add city labels
    for xi, yi, label in zip(x, y, labels):
        plt.text(xi, yi, label, fontsize=9, ha='right', va='bottom')

    plt.title("City Tour Route")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(save_path)
    print(f"📸 Route plot saved to: {save_path}")
    plt.show()

