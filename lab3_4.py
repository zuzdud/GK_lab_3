#!/usr/bin/env python3
from math import *
import random
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

N = 20
matrix = np.zeros((N + 1, N + 1, 3))
matrixColors = np.zeros((N + 1, N + 1, 3))


def startup():
    update_viewport(None, 1000, 1000)
    glClearColor(0.34, 0.0, 0.0, 1.0)
    # mechanizm bufora głębi
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    # oś x
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    # oś y
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    # oś z
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def matrixValues():
    for i in range(0, N+1):
        for j in range(0, N+1):
            u = i / N
            v = j / N

            # x
            matrix[i][j][0] = (-90 * pow(u, 5) + 225 * pow(u, 4) -
                               270*pow(u, 3) + 180*pow(u, 2) - 45*u) * cos(pi * v)
            # y
            matrix[i][j][1] = 160 * \
                pow(u, 4) - 320*pow(u, 3) + 160*pow(u, 2) - 5
            # z
            matrix[i][j][2] = (-90 * pow(u, 5) + 225 * pow(u, 4) -
                               270*pow(u, 3) + 180*pow(u, 2) - 45*u) * sin(pi * v)


def matrixColorValues():
    for i in range(0, N + 1):
        for j in range(0, N + 1):
            u = i/N
            v = j/N
            matrixColors[i][j][0] = random.random()
            matrixColors[i][j][1] = random.random()
            matrixColors[i][j][2] = random.random()

    for i in range(0, int(N / 2) - 1):
        matrixColors[N - i][N][0] = matrixColors[i][0][0]
        matrixColors[N - i][N][1] = matrixColors[i][0][1]
        matrixColors[N - i][N][2] = matrixColors[i][0][2]

    r = 0.0
    g = 0.0
    b = 0.0
    
    for i in range(0, N+1):
        matrixColors[N][i][0] = r
        matrixColors[N][i][1] = g
        matrixColors[N][i][2] = b

        matrixColors[int(N/2)][i][0] = r
        matrixColors[int(N/2)][i][1] = g
        matrixColors[int(N/2)][i][2] = b

        matrixColors[0][i][0] = r
        matrixColors[0][i][1] = g
        matrixColors[0][i][2] = b


def drawJajo():
    for i in range(0, N):
        for j in range(0, N):
            glBegin(GL_TRIANGLE_STRIP)

            glColor3f(matrixColors[i][j][0], matrixColors[i]
                      [j][1], matrixColors[i][j][2])
            glVertex3f(matrix[i][j][0], matrix[i][j][1], matrix[i][j][2])

            glColor3f(matrixColors[i+1][j][0], matrixColors[i+1]
                      [j][1], matrixColors[i+1][j][2])
            glVertex3f(matrix[i+1][j][0], matrix[i+1][j][1], matrix[i+1][j][2])

            glColor3f(matrixColors[i][j+1][0], matrixColors[i]
                      [j+1][1], matrixColors[i][j+1][2])
            glVertex3f(matrix[i][j+1][0], matrix[i][j+1][1], matrix[i][j+1][2])

            glColor3f(matrixColors[i+1][j+1][0], matrixColors[i+1]
                      [j+1][1], matrixColors[i+1][j+1][2])
            glVertex3f(matrix[i+1][j+1][0], matrix[i+1]
                       [j+1][1], matrix[i+1][j+1][2])
            glEnd()


def render(time):
    # mechanizm bufora głębi
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180/3.1415/3)
    drawJajo()
    axes()

    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    # zmieniony zakres rysowania
    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(1000, 1000, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    matrixValues()
    matrixColorValues()

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
