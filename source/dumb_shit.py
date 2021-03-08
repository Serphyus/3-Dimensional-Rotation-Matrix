import os
import pygame
from random import randint
from math import sin, cos, radians



class Model:
    def __init__(self, shape: dict, color: tuple):
        self.verticies = shape.get('verticies', [])
        self.edges = shape.get('edges', [])
        self.color = color
        self.rotation = [0, 0, 0]
    

    def rotateModel(self, rotation: tuple) -> None:
        for index, value in enumerate(rotation):
            self.rotation[index] += value


    def getModel(self) -> list:
        """
        :param rotation: pitch, yaw, roll rotation values (γ, β, α)

        γ: pitch (x rotation)
        β: yaw   (y rotation)
        α: roll  (z rotation)

                            [ cosα -sinα  0 ] [ cosβ   0   sinβ ] [ 1   0     0   ]
        Rz(α) Ry(β) Rx(γ) = [ sinα  cosα  0 ] [ 0      1    0   ] [ 0  cosγ -sinγ ]
                            [  0     0    1 ] [ -sinβ  0   cosβ ] [ 0  sinγ  cosγ ]

            [cosα cosβ    cosα sinβ sinγ - sinα cosγ    cosα sinβ cosγ + sinα sinγ]
        R = [sinα cosβ    sinα sinβ sinγ + cosα cosγ    sinα sinβ cosγ - cosα sinγ]
            [ -sinβ              cosβ sinγ                      cosβ cosγ         ]

        """
        γ = radians(self.rotation[0])
        β = radians(self.rotation[1])
        α = radians(self.rotation[2])
        
        matrix = [
            [cos(α) * cos(β),    cos(α) * sin(β) * sin(γ) - sin(α) * cos(γ),    cos(α) * sin(β) * cos(γ) + sin(α) * sin(γ)],
            [sin(α) * cos(β),    sin(α) * sin(β) * sin(γ) + cos(α) * cos(γ),    sin(α) * sin(β) * cos(γ) - cos(α) * sin(γ)],
            [    -sin(β),                   cos(β) * sin(γ),                                   cos(β) * cos(γ)            ]
        ]

        rotated_verticies = []
        for (x, y, z) in self.verticies:
            new_point = []
            for vector in matrix:
                new_point.append(
                    ((x * vector[0]) + (y * vector[1]) + (z * vector[2]))
                )
            rotated_verticies.append(new_point)
        
        return [rotated_verticies, self.edges]



class Gui:
    def __init__(self, resolution: tuple, fps: int, path: str, scrolling_sensitivity: int, rotation_speed: int, display_verticies: bool, display_edges: bool):
        pygame.init()

        self.models = []

        self.display = pygame.display.set_mode(resolution)
        self.resolution = resolution
        self.center = [int(resolution[i] / 2) for i in range(2)]
        self.upscale = int(resolution[0] / 8)

        self.clock = pygame.time.Clock()
        self.fps = fps

        self.scrolling_sensitivity = scrolling_sensitivity
        self.rotation_speed = rotation_speed

        self.display_verticies = display_verticies
        self.display_edges = display_edges

        self.font = pygame.font.Font(os.path.join(path, 'assets/coolvetica.ttf'), 25)
    

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
            if self.display_verticies:
                for cordinates in verticies:
                    center = tuple([(self.center[i] + cordinates[i * 2] * self.upscale) for i in range(2)])
                    pygame.draw.circle(self.display, model.color, center, 5)
        
            if self.display_edges:
                for edge in edges:
                    points = []
                    for e in edge:
                        points.append(tuple([self.center[i] + verticies[e][i * 2] * self.upscale for i in range(2)]))
                    pygame.draw.line(self.display, model.color, points[0], points[1], 2)

    
    def drawText(self, text: str, position: tuple) -> None:
        textSurface = self.font.render(text, True, (255, 255, 255))
        textRectangle = textSurface.get_rect()
        
        for index, axis in enumerate(['x', 'y']):
                setattr(textRectangle, axis, position[index])

        self.display.blit(textSurface, textRectangle)


    def displayInfo(self) -> None:
        # FPS
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
                self.upscale += (event.y * self.scrolling_sensitivity)

            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_u]:   self.rotateAll((self.rotation_speed, 0, 0))
            if keys[pygame.K_i]: self.rotateAll((0, self.rotation_speed, 0))
            if keys[pygame.K_o]: self.rotateAll((0, 0, self.rotation_speed))
            if keys[pygame.K_j]: self.rotateAll((-self.rotation_speed, 0, 0))
            if keys[pygame.K_k]: self.rotateAll((0, -self.rotation_speed, 0))
            if keys[pygame.K_l]: self.rotateAll((0, 0, -self.rotation_speed))


    def updateDisplay(self) -> None:
        # draw 3d models and display info on top
        self.drawModels()
        self.displayInfo()
        
        # update the display
        pygame.display.update()
        self.display.fill((0, 0, 0))
        
        self.clock.tick(self.fps)