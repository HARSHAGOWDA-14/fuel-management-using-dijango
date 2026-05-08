
import os
import pandas as pd
import requests
from geopy.geocoders import Nominatim
from shapely.geometry import Point, LineString

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, 'routes', 'fuel_prices_for_be_assessment.csv')

API_KEY = 'YOUR_OPENROUTESERVICE_API_KEY'

fuel_df = pd.read_csv(CSV_PATH)

def geocode_location(location):
    geolocator = Nominatim(user_agent='fuel_api')
    loc = geolocator.geocode(location)
    return [loc.longitude, loc.latitude]

def get_route(start, finish):
    coords = [
        geocode_location(start),
        geocode_location(finish)
    ]

    headers = {
        'Authorization': API_KEY,
        'Content-Type': 'application/json'
    }

    body = {
        'coordinates': coords
    }

    response = requests.post(
        'https://api.openrouteservice.org/v2/directions/driving-car/geojson',
        json=body,
        headers=headers
    )

    return response.json()

def find_cheapest_stops(route_coords, total_distance):
    route_line = LineString(route_coords)

    nearby = []

    for _, row in fuel_df.iterrows():
        try:
            point = Point(row['longitude'], row['latitude'])

            if route_line.distance(point) < 0.3:
                nearby.append({
                    'truckstop_name': row.get('truckstop_name', ''),
                    'city': row.get('city', ''),
                    'state': row.get('state', ''),
                    'price': float(row.get('retail_price', 3.5)),
                    'latitude': row['latitude'],
                    'longitude': row['longitude']
                })
        except:
            continue

    nearby = sorted(nearby, key=lambda x: x['price'])

    return nearby[:3]

def optimize_route(start, finish):
    route = get_route(start, finish)

    feature = route['features'][0]

    distance_meters = feature['properties']['summary']['distance']
    distance_miles = distance_meters * 0.000621371

    gallons = distance_miles / 10

    coords = feature['geometry']['coordinates']

    fuel_stops = find_cheapest_stops(coords, distance_miles)

    avg_price = (
        sum(stop['price'] for stop in fuel_stops) / len(fuel_stops)
        if fuel_stops else 3.5
    )

    total_cost = gallons * avg_price

    return {
        'start': start,
        'finish': finish,
        'distance_miles': round(distance_miles, 2),
        'estimated_gallons_used': round(gallons, 2),
        'total_fuel_cost': round(total_cost, 2),
        'fuel_stops': fuel_stops,
        'route_geometry': feature['geometry']
    }
