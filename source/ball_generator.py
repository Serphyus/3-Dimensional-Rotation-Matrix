import os
import json
from math import radians, cos, sin



radius = int(input('radius: '))
rings = int(input('rings: '))
points = int(input('ring_edges: '))
color = input('color: ').split()


model = {
    'shape': {
        'verticies': [],
        'edges': []
    },
    'color': [color]
}


for r in range(rings):
    for p in range(points):
        angle = int(radians((360 / points) * p))
        verticy = [radius * cos(angle), radius * sin(angle), ((radius / rings) * r)]
        model['shape']['verticies'].append(verticy)


current_path = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(current_path, 'assets/models/ball.json'), 'w') as _file:
    json.dump(model, _file, indent=4)