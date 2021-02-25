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

    # 
    edges = (
        (0, 1), (0, 3), (0, 4),
        (2, 3), (2, 1), (2, 6),
        (7, 3), (7, 4), (7, 6),
        (5, 1), (5, 4), (5, 6)
    )

    point_colors = [[randint(0, 255) for i in range(3)] for i in range(len(verticies))]
    line_colors = [[randint(0, 255) for i in range(3)] for i in range(len(edges))]

    @classmethod
    def updateVerticies(cls, points: list) -> None:
        if type(points) != list:
            raise TypeError('points argument must be a list')
        elif len(points) != len(cls.verticies):
            raise IndexError(f'poinst must contain {len(cls.verticies)} [x, y, z] cordinates')
        cls.verticies = points


class Gui:
    def __init__(self, resolution: tuple, fps: int):
        pygame.init()

        self.display = pygame.display.set_mode(resolution)
        self.resolution = resolution
        self.center = [int(resolution[i] / 2) for i in range(2)]
        
        # add another axis so that z can be displayed as y
        self.center.append(self.center[1])

        self.upscale = 100
        self.clock = pygame.time.Clock()
        self.fps = fps

        self.font = pygame.font.Font(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'coolvetica.ttf'), 20)
    

    def drawCube(self) -> None:
        # when drawing the cube use the (x, z) cordinates of each verticy
        # to draw on a 2 dimentional surface since the y axis is not physically
        # possible to draw in a 3 dimentional space on a 2 dimentional surface

        for index, cordinates in enumerate(Cube.verticies):
            center = tuple([(self.center[i] + cordinates[i] * self.upscale) for i in (0, 2)])
            pygame.draw.circle(self.display, Cube.line_colors[index], center, 5)
        
        for index, edges in enumerate(Cube.edges):
            points = []
            for i in edges:
                points.append(tuple([self.center[c] + Cube.verticies[i][c] * self.upscale for c in (0, 2)]))
            pygame.draw.line(self.display, (Cube.line_colors[index]), points[0], points[1], 2)

    
    def drawText(self, text: str, position: tuple, aa=True, color=(255, 255, 255)) -> None:
        textSurface = self.font.render(text, aa, color)
        textRectangle = textSurface.get_rect()
        
        for index, axis in enumerate(['x', 'y']):
                setattr(textRectangle, axis, position[index])

        self.display.blit(textSurface, textRectangle)


    def displayInfo(self) -> None:
        self.drawText(
            text=f'FPS - {self.clock.get_fps():.2f}',
            position=(8, 5), color=(255, 255, 255)
        )
        
        self.drawText('[U/J]  -  X rotation (pitch)', (8, 30),)
        self.drawText('[I/K]   -  Y rotation (roll)', (8, 50),)
        self.drawText('[O/L]  -  Z rotation (yaw)', (8, 70),)



    def mainLoop(self, rotation_speed) -> None:
        while True:
            pressed_keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            if pressed_keys[pygame.K_u]:   Cube.updateVerticies(generalRotation((rotation_speed, 0, 0)))
            elif pressed_keys[pygame.K_i]: Cube.updateVerticies(generalRotation((0, rotation_speed, 0)))
            elif pressed_keys[pygame.K_o]: Cube.updateVerticies(generalRotation((0, 0, rotation_speed)))
            elif pressed_keys[pygame.K_j]: Cube.updateVerticies(generalRotation((-rotation_speed, 0, 0)))
            elif pressed_keys[pygame.K_k]: Cube.updateVerticies(generalRotation((0, -rotation_speed, 0)))
            elif pressed_keys[pygame.K_l]: Cube.updateVerticies(generalRotation((0, 0, -rotation_speed)))

            self.display.fill((0, 0, 0))
            self.displayInfo()
            self.drawCube()
            pygame.display.update()

            self.clock.tick(self.fps)





def generalRotation(rotation: tuple):
    """
     :param rotation: roll, yaw, pitch rotation values (α, β, γ)

     α: roll  (z rotation)
     β: yaw   (y rotation)
     γ: pitch (x rotation)

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

    output = []
    for (x, y, z) in Cube.verticies:
        new_point = []
        for vector in matrix:
            new_point.append(
                ((x * vector[0]) + (y * vector[1]) + (z * vector[2]))
            )
        output.append(new_point)
    
    return output


if __name__ == '__main__':
    gui = Gui(resolution=(800, 800), fps=60)
    gui.mainLoop(1)