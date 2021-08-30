import os
import json
import pandas as pd


def get_geojson():
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'example.json')

    print('hola')

    with open(my_file, "r") as f:
        data = json.loads(f.read())
        data = data['features']

        data_coordinates = []
        for point in data:
            data_coordinates.append(point['properties'])

        return data_coordinates
