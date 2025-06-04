import argparse
import sys
from pathlib import Path
import time

from utils import load_places
from distance import build_distance_matrix
from tsp_solver import greedy_tsp, two_opt, route_distance
from geojson_writer import write_route_geojson

def parse_args():
    parser = argparse.ArgumentParser(
        description="🗺️ City Tour Optimizer — Plan the shortest route through your chosen places!"
    )
    parser.add_argument(
        '--csv', required=True,
        help='Path to places.csv (must contain columns: Name,Lat,Lon)'
    )
    parser.add_argument(
        '--start', required=True,
        help='Name of the starting location (must match a row in CSV exactly)'
    )
    parser.add_argument(
        '--return-to-start', dest='return_to_start', action='store_true',
        help='Return to starting location at the end of the route'
    )
    parser.add_argument(
        '--output', default='output/route.geojson',
        help='Path to write the output GeoJSON route'
    )
    parser.add_argument(
        '--plot', action='store_true', 
        help='Show matplotlib plot of the route'
    )
    parser.add_argument(
        '--open-from', type=str, 
        help='Desired earliest visit time (e.g., 10:00)'
    )
    parser.add_argument(
        '--open-until', type=str, 
        help='Desired latest visit time (e.g., 18:00)'
    )
    parser.add_argument(
    '--algo', default='greedy', choices=['greedy', '2opt', 'simulated-annealing'],
    help='Choose algorithm: "greedy", "2opt", or "simulated-annealing"'
    )

    return parser.parse_args()

def main():
    args = parse_args()
    from datetime import datetime

    # Verify input CSV file exists
    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"❌ Error: CSV file '{args.csv}' not found.")
        sys.exit(1)

    # Load places from CSV
    places = load_places(csv_path)
    if len(places) < 2:
        print("❌ Error: Need at least 2 places to compute a route.")
        sys.exit(1)

    # ✅ Time-window filtering
    if args.open_from and args.open_until:
        window_start = datetime.strptime(args.open_from, "%H:%M").time()
        window_end = datetime.strptime(args.open_until, "%H:%M").time()

        filtered_places = []
        for place in places:
            if place.open_time <= window_start and place.close_time >= window_end:
                filtered_places.append(place)

        places = filtered_places

        if len(places) < 2:
            print("❌ Not enough places open during the selected time window.")
            sys.exit(1)

    # Get start index
    start_idx = next((i for i, p in enumerate(places) if p.name == args.start), None)
    if start_idx is None:
        print(f"❌ Error: Start location '{args.start}' not found in the CSV.")
        sys.exit(1)

    # Build distance matrix
    dist = build_distance_matrix(places)

    start_time = time.time()

    # Run selected TSP algorithm
    print(f"\n📍 Computing route using '{args.algo}' algorithm...")
    route = greedy_tsp(start_idx, dist)
    if args.algo == '2opt':
        route = two_opt(route, dist)
    elif args.algo == 'simulated-annealing':
        from tsp_solver import simulated_annealing
        route = simulated_annealing(route, dist)

    if args.return_to_start:
        route.append(route[0])

    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)

    # Display route
    print("\n🧭 Optimal Tour:")
    for i, idx in enumerate(route):
        print(f"{i+1}) {places[idx].name}")

    total_km = route_distance(route, dist)
    print(f"\n📏 Total Distance: {total_km:.2f} km")

    from datetime import datetime

    log_path = Path("logs/route_stats.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ")
        f.write(f"Algo={args.algo}, Distance={total_km:.2f} km, Time={elapsed_time}s\n")

    print(f"📝 Stats logged to: {log_path.resolve()}")


    # Export to GeoJSON
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_route_geojson([places[i] for i in route], output_path)
    print(f"✅ Route written to: {output_path.resolve()}")

    # Optional Matplotlib Plot
    if args.plot:
        from utils import plot_route
        plot_route(places, route)

if __name__ == "__main__":
    main()

