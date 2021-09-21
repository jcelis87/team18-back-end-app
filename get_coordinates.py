import os
import json
import pandas as pd


def get_geojson(my_file):
    
    print(my_file)
    with open(my_file, "r", encoding="utf8") as f:
        data = json.loads(f.read())
        data = data['features']

        data_coordinates = []
        for point in data:
            data_coordinates.append(point['properties'])

    return data_coordinates


def get_geojson_boundaries(my_file):

    with open(my_file, "r", encoding="utf8") as f:
        data = json.loads(f.read())
        data = data['features']

        data_boundaries = []
        for point in data:
            boundaries = point['geometry']['coordinates'][0]
            corners = []
            for corner in boundaries:
                corners.append(list(reversed(corner)))

            data_boundaries.append(corners)

        return data_boundaries


def get_geojson_image_boundaries(my_file):

    with open(my_file, "r", encoding="utf8") as f:
        data = json.loads(f.read())

        return data