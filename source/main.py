import os
import pygame
from random import randint
from math import radians, sin, cos



class Cube:
    # check beautifully drawn cube in .png file for visual reference
    verticies = [
        [-1, -1, -1],   # 1
        [ 1, -1, -1],   # 2
        [ 1, -1,  1],   # 3
        [-1, -1,  1],   # 4
        [-1,  1, -1],   # 5
        [ 1,  1, -1],   # 6
        [ 1,  1,  1],   # 7
        [-1,  1,  1],   # 8
    ]

    edges = (
        (0, 1), (0, 3), (0, 4),
        (2, 3), (2, 1), (2, 6),
        (7, 3), (7, 4), (7, 6),
        (5, 1), (5, 4), (5, 6)
    )

    orientation = [0, 0, 0]
    point_colors = [[randint(0, 255) for i in range(3)] for i in range(len(verticies))]
    line_colors = [[randint(0, 255) for i in range(3)] for i in range(len(edges))]


    @classmethod
    def rotateCube(cls, rotation: tuple) -> None:
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
        γ = radians(rotation[0])
        β = radians(rotation[1])
        α = radians(rotation[2])
        
        matrix = [
            [cos(α) * cos(β),    cos(α) * sin(β) * sin(γ) - sin(α) * cos(γ),    cos(α) * sin(β) * cos(γ) + sin(α) * sin(γ)],
            [sin(α) * cos(β),    sin(α) * sin(β) * sin(γ) + cos(α) * cos(γ),    sin(α) * sin(β) * cos(γ) - cos(α) * sin(γ)],
            [    -sin(β),                   cos(β) * sin(γ),                                   cos(β) * cos(γ)            ]
        ]

        new_verticies = []
        for (x, y, z) in cls.verticies:
            new_point = []
            for vector in matrix:
                new_point.append(
                    ((x * vector[0]) + (y * vector[1]) + (z * vector[2]))
                )
            new_verticies.append(new_point)
        
        cls.verticies = new_verticies



class Gui:
    def __init__(self, resolution: tuple, fps: int, display_verticies: bool, display_edges: bool):
        pygame.init()

        self.display = pygame.display.set_mode(resolution)
        self.resolution = resolution
        self.center = [int(resolution[i] / 2) for i in range(2)]
        
        # add another axis so that z can be displayed as y
        self.center.append(self.center[1])

        self.upscale = 100
        self.clock = pygame.time.Clock()
        self.fps = fps

        self.display_verticies = display_verticies
        self.display_edges = display_edges

        self.font = pygame.font.Font(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'coolvetica.ttf'), 25)
    

    def drawCube(self) -> None:
        # when drawing the cube use the (x, z) cordinates of each verticy
        # to draw on a 2 dimentional surface since the y axis is not physically
        # possible to draw in a 3 dimentional space on a 2 dimentional surface

        if self.display_verticies:
            for index, cordinates in enumerate(Cube.verticies):
                center = tuple([(self.center[i] + cordinates[i] * self.upscale) for i in (0, 2)])
                pygame.draw.circle(self.display, Cube.point_colors[index], center, 5)
        
        if self.display_edges:
            for index, edges in enumerate(Cube.edges):
                points = []
                for i in edges:
                    points.append(tuple([self.center[c] + Cube.verticies[i][c] * self.upscale for c in (0, 2)]))
                pygame.draw.line(self.display, (Cube.line_colors[index]), points[0], points[1], 2)

    
    def drawText(self, text: str, position: tuple) -> None:
        textSurface = self.font.render(text, True, (255, 255, 255))
        textRectangle = textSurface.get_rect()
        
        for index, axis in enumerate(['x', 'y']):
                setattr(textRectangle, axis, position[index])

        self.display.blit(textSurface, textRectangle)


    def displayInfo(self) -> None:
        # FPS
        self.drawText(
            text=f'FPS - {self.clock.get_fps():.2f}',
            position=(8, 5)
        )
        
        # Controls
        self.drawText('X rotation - U/J', (8, 30),)
        self.drawText('Y rotation - I/K', (8, 50),)
        self.drawText('Z rotation - O/L', (8, 70),)



    def mainLoop(self, rotation_speed) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[pygame.K_u]:   Cube.rotateCube((rotation_speed, 0, 0))
            elif pressed_keys[pygame.K_i]: Cube.rotateCube((0, rotation_speed, 0))
            elif pressed_keys[pygame.K_o]: Cube.rotateCube((0, 0, rotation_speed))
            elif pressed_keys[pygame.K_j]: Cube.rotateCube((-rotation_speed, 0, 0))
            elif pressed_keys[pygame.K_k]: Cube.rotateCube((0, -rotation_speed, 0))
            elif pressed_keys[pygame.K_l]: Cube.rotateCube((0, 0, -rotation_speed))

            self.display.fill((0, 0, 0))
            self.displayInfo()
            self.drawCube()
            pygame.display.update()

            self.clock.tick(self.fps)



if __name__ == '__main__':
    gui = Gui(
        resolution=(800, 800), fps=60,
        display_edges=True, display_verticies=True
    )
    
    gui.mainLoop(rotation_speed=1)