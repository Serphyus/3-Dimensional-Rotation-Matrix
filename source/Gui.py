import os
import json
import pygame
from Model import Model
from types import SimpleNamespace



class Gui:
    def __init__(self, path: str):
        pygame.init()

        with open(os.path.join(path, 'config.json'), 'r') as _file:
            self.config = SimpleNamespace(**json.load(_file))

        self.display = pygame.display.set_mode(self.config.resolution)
        self.center = [int(self.config.resolution[i] / 2) for i in range(2)]
        self.upscale = round(self.config.resolution[0] / 8)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(os.path.join(path, self.config.font_path), 25)
        
        self.models = []
    

    def addModel(self, model: Model) -> None:
        if model in self.models:
            raise IndexError('model already exists in Gui.models')
        self.models.append(model)
    
    
    def removeModel(self, model: Model) -> None:
        if model not in self.models:
            raise IndexError('model does not exists in Gui.models')
        self.models.remove(model)


    def rotateAll(self, rotation: list) -> None:
        for model in self.models:
            model.rotateModel(rotation)


    def drawModels(self) -> None:
        # when drawing the cube use the (x, z) cordinates of each verticy
        # to draw on a 2 dimentional surface since the y axis is not physically
        # possible to draw in a 3 dimentional space on a 2 dimentional surface

        for model in self.models:
            verticies, edges = model.getModel()
            if self.config.display_verticies:
                for cordinates in verticies:
                    point = tuple([(self.center[i] + cordinates[i * 2] * self.upscale + 1) for i in range(2)])
                    pygame.draw.circle(self.display, model.color, point, self.config.verticy_size)
        
            if self.config.display_edges:
                for edge in edges:
                    points = []
                    for e in edge:
                        points.append(tuple([self.center[i] + verticies[e][i * 2] * self.upscale for i in range(2)]))
                    pygame.draw.aaline(self.display, model.color, points[0], points[1], True)

    
    def drawText(self, text: str, position: tuple) -> None:
        textSurface = self.font.render(text, True, (255, 255, 255))
        textRectangle = textSurface.get_rect()
        
        for index, axis in enumerate(['x', 'y']):
                setattr(textRectangle, axis, position[index])

        self.display.blit(textSurface, textRectangle)


    def displayInfo(self) -> None:
        info = [
            [f'FPS - {self.clock.get_fps():.2f}', (8, 5)],
            ['X rotation - U/J', (8, 30)],
            ['Y rotation - I/K', (8, 50)],
            ['Z rotation - O/L', (8, 70)],
        ]

        for args in info:
            self.drawText(*args)


    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            
            if event.type == pygame.MOUSEWHEEL:
                self.upscale += (event.y * self.config.scrolling_sensitivity)

            keys = pygame.key.get_pressed()
            
            rotation = [0, 0, 0]
            
            if keys[pygame.K_u]: rotation[0] += self.config.rotation_speed
            if keys[pygame.K_i]: rotation[1] += self.config.rotation_speed
            if keys[pygame.K_o]: rotation[2] += self.config.rotation_speed
            if keys[pygame.K_j]: rotation[0] -= self.config.rotation_speed
            if keys[pygame.K_k]: rotation[1] -= self.config.rotation_speed
            if keys[pygame.K_l]: rotation[2] -= self.config.rotation_speed

            self.rotateAll(rotation)

            if keys[pygame.K_r]:
                for model in self.models:
                    model.revertRotation()
                    model.revertShape()


    def updateDisplay(self) -> None:
        self.drawModels()

        if self.config.display_info:
            self.displayInfo()
        
        pygame.display.update()
        self.display.fill((0, 0, 0))
        self.clock.tick(self.config.fps)