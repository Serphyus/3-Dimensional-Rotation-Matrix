import os
import json
from math import radians, cos, sin



radius = int(input('radius: '))
rings = int(input('rings: '))
color = [int(i) for i in input('color: ').split()]

model = {
    'shape': {
        'verticies': [],
        'edges': []
    },
    'color': color
}


for vertical in range(rings):
    v_angle = radians((360 / rings) * vertical)
    for horizontal in range(rings):
        h_angle = radians((360 / rings) * horizontal)

        x = radius * cos(v_angle) * cos(h_angle)
        y = radius * cos(v_angle) * sin(h_angle)
        z = radius * sin(v_angle)

        model['shape']['verticies'].append([x, y, z])


current_path = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_path, 'assets/models/sphere.json'), 'w') as _file:
    json.dump(model, _file, indent=4)