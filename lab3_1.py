#!/usr/bin/env python3
from math import *
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

N = 50
matrix =  np.zeros((N + 1, N + 1, 3))


def startup():
    update_viewport(None, 1000, 1000)
    glClearColor(0.34, 0.0, 0.0, 1.0)
    # mechanizm bufora głębi
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass

# rysujemy układ współrzędnych


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

# zanimowanie obiektu i obrót


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


# x(u, v) = (-90 * u^5 + 225 * u^4 - 270*u^3 + 180*u^2 -45*u) * cos(pi * v)
# y(u, v) = 160 * u^4 - 320*u^3 + 160*u^2 -5
# z(u, v) = (-90 * u^5 + 225 * u^4 - 270*u^3 + 180*u^2 -45*u) * sin(pi * v)

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


def drawJajo():
    glColor3ub(200, 130, 12)
    for i in range(0, N+1):
        for j in range(0, N+1):
            glPointSize(3)
            glBegin(GL_POINTS)
            glVertex3f(matrix[i][j][0], matrix[i][j][1], matrix[i][j][2])
            glEnd()


def render(time):

    # mechanizm bufora głębi
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180/3.1415)
    axes()
    drawJajo()

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
