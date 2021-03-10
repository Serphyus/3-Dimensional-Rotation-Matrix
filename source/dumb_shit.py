import os
import json
from Gui import Gui
from Model import Model
from random import uniform



def load_all(models_path: str, available_models: str) -> list:
    models = []
    for _model in available_models:
        with open(os.path.join(models_path, _model), 'r') as _file:
            models.append(Model(**json.load(_file)))
    return models


def disturb_model_flat(self, model: Model) -> None:
    mod = []
    for i in range(len(model.verticies)):
        if i < 5 or i > 20:
            mod.append(None)
        elif i % 5 == 0:
            mod.append(None)
        elif (i+1) % 5 == 0:
            mod.append(None)
        else:
            #current = model.modifications[i]
            #if current > 
            mod.append([0, 0, (uniform(0, -1) / 10)])
    model.modifyVerticies(mod)



if __name__ == '__main__':
    working_path = os.path.abspath(os.path.dirname(__file__))
    models_path = os.path.join(working_path, 'assets/models')

    available_models = os.listdir(models_path)
    for index, model in enumerate(available_models + ['all']):
        print('%i) %s' % (index+1, model))
    model_choice = int(input('\n> '))

    models = []
    if model_choice == len(available_models)+1:
        models = load_all(models_path, available_models)
    elif model_choice < 1:
        raise IndexError('list index out of range')
    else:
        with open(os.path.join(models_path, available_models[model_choice-1]), 'r') as _file:
            models.append(Model(**json.load(_file)))

    gui = Gui(working_path)

    for model in models:
        gui.addModel(model)

    while True:
        gui.handleEvents()
        gui.updateDisplay()