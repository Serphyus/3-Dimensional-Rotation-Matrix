import os
import json
from Gui import Gui
from Model import Model
from random import uniform



if __name__ == '__main__':
    working_path = os.path.abspath(os.path.dirname(__file__))
    models_path = os.path.join(working_path, 'assets/models')

    available_models = os.listdir(models_path)
    for index, model in enumerate(available_models):
        print('%i) %s' % (index+1, model))
    model_choice = int(input('\n> '))

    with open(os.path.join(models_path, available_models[model_choice-1]), 'r') as _file:
        model = Model(**json.load(_file))


    gui = Gui(working_path)
    gui.addModel(model)

    while True:
        gui.handleEvents()
        gui.updateDisplay()