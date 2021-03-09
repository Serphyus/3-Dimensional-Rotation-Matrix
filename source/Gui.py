import os
import pygame
from Model import Model



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
                    point = tuple([(self.center[i] + cordinates[i * 2] * self.upscale) for i in range(2)])
                    pygame.draw.circle(self.display, model.color, point, 5)
        
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
            
            rotation = [0, 0, 0]
            
            if keys[pygame.K_u]: rotation[0] += self.rotation_speed
            if keys[pygame.K_i]: rotation[1] += self.rotation_speed
            if keys[pygame.K_o]: rotation[2] += self.rotation_speed
            if keys[pygame.K_j]: rotation[0] -= self.rotation_speed
            if keys[pygame.K_k]: rotation[1] -= self.rotation_speed
            if keys[pygame.K_l]: rotation[2] -= self.rotation_speed

            self.rotateAll(rotation)

            if keys[pygame.K_r]:
                for model in self.models:
                    model.revertRotation()


    def updateDisplay(self) -> None:
        self.drawModels()
        self.displayInfo()
        
        pygame.display.update()
        self.display.fill((0, 0, 0))
        
        self.clock.tick(self.fps)