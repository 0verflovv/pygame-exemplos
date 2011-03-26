import pygame, sys
from math import *

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Spinning cube! 8-)")
clock = pygame.time.Clock()

counter = 0


def Radians(angle):
    return ((float(angle) / 180.0) * pi)

def Transform(vertex, matrix):
    Vx = (vertex[0]*matrix[0][0]) + (vertex[1] * matrix[1][0]) + (vertex[2] * matrix[2][0])
    Vy = (vertex[0]*matrix[0][1]) + (vertex[1] * matrix[1][1]) + (vertex[2] * matrix[2][1])
    Vz = (vertex[0]*matrix[0][2]) + (vertex[1] * matrix[1][2]) + (vertex[2] * matrix[2][2])

    return (Vx, Vy, Vz)


class Cube():
    def __init__(self, position, size):
        self.position = position
        self.size = float(size) / 2.0
        self.vertices = [  # Creating the eight vertices
            [self.position[0] + self.size, self.position[1] + self.size, self.position[2] + self.size],
            [self.position[0] + self.size, self.position[1] + self.size, self.position[2] - self.size],
            [self.position[0] + self.size, self.position[1] - self.size, self.position[2] + self.size],
            [self.position[0] + self.size, self.position[1] - self.size, self.position[2] - self.size],
            [self.position[0] - self.size, self.position[1] + self.size, self.position[2] + self.size],
            [self.position[0] - self.size, self.position[1] + self.size, self.position[2] - self.size],
            [self.position[0] - self.size, self.position[1] - self.size, self.position[2] + self.size],
            [self.position[0] - self.size, self.position[1] - self.size, self.position[2] - self.size]
        ]
        # Defining which vertices to connect with lines - written by a process of trial and error; edit at your peril
        self.lines = [[0, 1], [1, 3], [2, 3], [2, 0], [0, 4], [4, 5], [5, 1], [4, 6], [6, 7], [7, 5], [6, 2], [7, 3]]

    def Rotate(self, axis, angle):
        angle = Radians(angle)# Convert the angle to radians (Python doesn't like degrees, apparently)

        if axis == 0:  # X
            matrix = [
                [1, 0, 0],
                [0, cos(angle), sin(angle)],
                [0, -sin(angle), cos(angle)]
            ]
        elif axis == 1:  # Y
            matrix = [
                [cos(angle), 0, -sin(angle)],
                [0, 1, 0],
                [sin(angle), 0, cos(angle)]
            ]
        elif axis == 2:  # Z
            matrix = [
                [cos(angle), sin(angle), 0],
                [-sin(angle), cos(angle), 0],
                [0, 0, 1]
            ]

        temp = []  # Temporary list of transformed vertices
        for vertex in self.vertices:
            temp.append(Transform(vertex, matrix))

        self.vertices = temp
    
    def Scale(self, axis, k):
        if axis == 0:  # X
            matrix = [
                [k, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
            ]
        if axis == 1:  # Y
            matrix = [
                [1, 0, 0],
                [0, k, 0],
                [0, 0, 1]
            ]
        if axis == 0:  # Z
            matrix = [
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, k]
            ]

        temp = []
        for vertex in self.vertices:
            temp.append(Transform(vertex, matrix))

        self.vertices = temp


cubes = []  # The list of cubes in the scene

cube1 = Cube((0, 0, 0), 250)
cube1.Rotate(0, 20)
cube1.Rotate(2, 35)

cube2 = Cube((200, 100, 500), 250)
cube2.Rotate(2, 55)

cubes.append(cube1)
cubes.append(cube2)


def DimensionChange(vertex):
    # Converts a 3D point into a 2D coordinate by projecting onto the XY axis
    # (a n00bish solution that renders camera movement impossible for the moment :P)
    matrix = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]

    Vx, Vy, Vz = Transform(vertex, matrix)
    
    return (Vx, Vy)

def Redraw():
    # Keep the cubes spinning
    cube1.Rotate(1, 3)
    cube1.Rotate(2, -2)
    cube2.Rotate(1, 3)
    cube2.Rotate(2, -2)

    for cube in cubes:
        points = []  # List of 2D points
        for vertex in cube.vertices:  # Get the 2D points to draw
            points.append(DimensionChange(vertex))

        temp = []
        for point in points:  # Centre the points on-screen (such that the point (0, 0, 0) is displayed at the centre of the screen)
            temp.append([400+point[0], 300+point[1]])
        points = temp

        for point in points:  # Draw points
            pygame.draw.circle(screen, (255,255,255), (point[0], point[1]), 2)

        for line in cube.lines:  # Draw lines
            pygame.draw.aaline(screen, (255, 255, 255), points[line[0]], points[line[1]])


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill((0, 0, 0))

    Redraw()
    
    counter += 1  # Was once used, but isn't now. But you never know when it could come in handy
    
    pygame.display.update()
    clock.tick(25)

