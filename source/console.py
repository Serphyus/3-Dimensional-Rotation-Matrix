import os
import sys
import ctypes
from time import time
from random import randint
from math import radians, sin, cos



class Cube:
    verticies = [
        [-1, -1, -1],
        [ 1, -1, -1],
        [ 1, -1,  1],
        [-1, -1,  1],
        [-1,  1, -1],
        [ 1,  1, -1],
        [ 1,  1,  1],
        [-1,  1,  1],
    ]


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



class Console:
    def __init__(self):
        resolution = tuple(os.get_terminal_size())

        self.resolution = os.get_terminal_size()
        self.center = [int(resolution[i] / 2) for i in range(2)]
        self.upscale = [
            int(resolution[0] / 12),
            int(resolution[0] / 24)
        ]

        self.previous_positions = None

    def drawCube(self) -> None:
        new_positions = []
        for cordinates in Cube.verticies:
            new_positions.append([
                int(self.center[0] + (cordinates[0] * self.upscale[0])),   # x
                int(self.center[1] + (cordinates[2] * self.upscale[1]))    # z
            ])

        if self.previous_positions != None:
            if self.previous_positions != new_positions:
                for pos in self.previous_positions:
                    self.updateLine(pos[1], pos[0], ' ')
                for pos in new_positions:
                    self.updateLine(pos[1], pos[0], '#')
        self.previous_positions = new_positions



    def updateLine(self, y: int, x: int, text: str, **kwargs) -> None:
        print("\033[%d;%dH%s" % (y+1, x, text), **kwargs)
        sys.stdout.flush()


    def hideCursor(self) -> None:
        sys.stdout.write('\033[?25l')
        sys.stdout.flush()
    

    def showCursor(self) -> None:
        sys.stdout.write('\033[?25h')
        sys.stdout.flush()

    
    def mainLoop(self, rotation: tuple, fps: int) -> None:
        self.hideCursor()
        fps_tick = 1 / fps
        last_tick = time()
        try:
            while True:
                if time() >= (last_tick + fps_tick):
                    Cube.rotateCube(rotation)
                    self.drawCube()
                    last_tick = time()
        except KeyboardInterrupt:
            sys.stdout.write('\033[?25h')
            sys.stdout.flush()



if __name__ == '__main__':
    if sys.platform == 'win32':
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    console = Console()
    console.mainLoop(
        rotation=(-0.13, 0.73, 0.83),
        fps=120
    )