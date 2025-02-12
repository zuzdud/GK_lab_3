#!/usr/bin/env python3
from math import *
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

N = 50
matrix = np.zeros((N + 1, N + 1, 3))
matrixv2 = np.zeros((N + 1, N + 1, 3))
matrixv3 = np.zeros((N + 1, N + 1, 3))
matrixv4 = np.zeros((N + 1, N + 1, 3))
matrixv5 = np.zeros((N + 1, N + 1, 3))


def startup():
    update_viewport(None, 2000, 1000)
    glClearColor(0.0, 0.0, 0.0, 1.0)
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
scale = 0.5

def matrixValues():
    for i in range(0, N+1):
        for j in range(0, N+1):
            u = i / N
            v = j / N

            # x
            matrix[i][j][0] = scale * (2 * sin(u * pi) * cos(2*pi * v) - 1)
            # y
            matrix[i][j][1] = scale * (2.5 * sin(pi * u) * sin(2 * pi * v) -2)
            # z
            matrix[i][j][2] = scale * 2 * cos(pi * u)


def matrixValuesv2():
    for i in range(0, N+1):
        for j in range(0, N+1):
            u = i / N
            v = j / N

            # x
            matrixv2[i][j][0] = scale * (2 * sin(u * pi) * cos(2*pi * v) + 1)
            # y
            matrixv2[i][j][1] = scale * (2.5 * sin(pi * u) * sin(2 * pi * v) -2)
            # z
            matrixv2[i][j][2] = scale * 2 * cos(pi * u)


def matrixValuesv3():
    for i in range(0, N+1):
        for j in range(0, N+1):
            u = i / N
            v = j / N
            fi =  i * 0.25 * pi / N

            rotationMatrix = np.zeros((3, 3))

            rotationMatrix[1][1] = cos(fi)
            rotationMatrix[0][0] = 1
            rotationMatrix[1][2] = -sin(fi)
            rotationMatrix[2][1] = sin(fi)
            rotationMatrix[2][2] = cos(fi)

            radius = 0.8 # * sin(u * pi) <= circle radius

            # draw a circle on XY plane. Z is zero here.
            # x
            matrixv3[i][j][0] = scale * 2 * cos(2*pi * v) * radius
            # y
            matrixv3[i][j][1] = scale * 2 * sin(2 * pi * v) * radius

            # rotate the circle around X axis. Z is also filled here, as it becomes non-zero due to rotation around X.
            matrixv3[i][j] = np.matmul(rotationMatrix, matrixv3[i][j])

            # move the circle along Y axis
            matrixv3[i][j][1] = matrixv3[i][j][1] + scale * 6 * sin(fi)
            # move the circle along Z axis
            matrixv3[i][j][2] = matrixv3[i][j][2] + scale * (5 * cos(pi * u) - 4)


def matrixValuesv4():
    for i in range(0, N+1):
        for j in range(0, N+1):
            u = i / N
            v = j / N

            # x
            matrixv4[i][j][0] = scale * 2 * sin(u * pi) * cos(2*pi * v)
            # y
            matrixv4[i][j][1] = scale * (2 * sin(pi * u) * sin(2 * pi * v) + 4.5)
            # z
            matrixv4[i][j][2] = scale * (2.5 * cos(pi * u) - 9.5)


def matrixValuesv5():
    for i in range(0, N+1):
        for j in range(0, N+1):
            u = i / N
            v = j / N

            # x
            matrixv5[i][j][0] = scale * 2 * sin(u * pi) * cos(2*pi * v)
            # y
            matrixv5[i][j][1] = scale * (2 * sin(pi * u) * sin(2 * pi * v) - 1)
            # z
            matrixv5[i][j][2] = scale * (5 * cos(pi * u) - 4)


def drawJajo():
    glColor3ub(158, 103, 96)
    for i in range(0, N):
        for j in range(0, N):
            glBegin(GL_TRIANGLES)
            glVertex3f(matrix[i][j][0], matrix[i][j][1], matrix[i][j][2])
            glVertex3f(matrix[i+1][j][0], matrix[i+1][j][1], matrix[i+1][j][2])
            glVertex3f(matrix[i][j+1][0], matrix[i][j+1][1], matrix[i][j+1][2])

            glVertex3f(matrix[i+1][j+1][0], matrix[i+1]
                       [j+1][1], matrix[i+1][j+1][2])
            glVertex3f(matrix[i+1][j][0], matrix[i+1][j][1], matrix[i+1][j][2])
            glVertex3f(matrix[i][j+1][0], matrix[i][j+1][1], matrix[i][j+1][2])
            glEnd()

    glColor3ub(158, 103, 96)
    for i in range(0, N):
        for j in range(0, N):
            glBegin(GL_TRIANGLES)
            glVertex3f(matrixv2[i][j][0], matrixv2[i][j][1], matrixv2[i][j][2])
            glVertex3f(matrixv2[i+1][j][0], matrixv2[i+1]
                       [j][1], matrixv2[i+1][j][2])
            glVertex3f(matrixv2[i][j+1][0], matrixv2[i]
                       [j+1][1], matrixv2[i][j+1][2])

            glVertex3f(matrixv2[i+1][j+1][0], matrixv2[i+1]
                       [j+1][1], matrixv2[i+1][j+1][2])
            glVertex3f(matrixv2[i+1][j][0], matrixv2[i+1]
                       [j][1], matrixv2[i+1][j][2])
            glVertex3f(matrixv2[i][j+1][0], matrixv2[i]
                       [j+1][1], matrixv2[i][j+1][2])
            glEnd()

    # complex shaft
    # glColor4ub(200, 130, 122, 255)
    # for i in range(0, N):
    #     for j in range(0, N):

    #         if (i < 40):
    #             glColor4ub(200, 130, 122, 255)
    #         else:
    #             glColor3ub(122, 24, 60)

    #         # glPointSize(3)
    #         glBegin(GL_TRIANGLES)
    #         glVertex3f(matrixv3[i][j][0], matrixv3[i][j][1], matrixv3[i][j][2])
    #         glVertex3f(matrixv3[i+1][j][0], matrixv3[i+1][j][1], matrixv3[i+1][j][2])
    #         glVertex3f(matrixv3[i][j+1][0], matrixv3[i][j+1][1], matrixv3[i][j+1][2])

    #         glVertex3f(matrixv3[i+1][j+1][0], matrixv3[i+1][j+1][1], matrixv3[i+1][j+1][2])
    #         glVertex3f(matrixv3[i+1][j][0], matrixv3[i+1][j][1], matrixv3[i+1][j][2])
    #         glVertex3f(matrixv3[i][j+1][0], matrixv3[i][j+1][1], matrixv3[i][j+1][2])

    #         glEnd()

    # glColor3ub(122, 24, 60)
    # for i in range(0, N):
    #     for j in range(0, N):
    #         glBegin(GL_TRIANGLES)
    #         glVertex3f(matrixv4[i][j][0], matrixv4[i][j][1], matrixv4[i][j][2])
    #         glVertex3f(matrixv4[i+1][j][0], matrixv4[i+1][j][1], matrixv4[i+1][j][2])
    #         glVertex3f(matrixv4[i][j+1][0], matrixv4[i][j+1][1], matrixv4[i][j+1][2])

    #         glVertex3f(matrixv4[i+1][j+1][0], matrixv4[i+1]
    #                    [j+1][1], matrixv4[i+1][j+1][2])
    #         glVertex3f(matrixv4[i+1][j][0], matrixv4[i+1][j][1], matrixv4[i+1][j][2])
    #         glVertex3f(matrixv4[i][j+1][0], matrixv4[i][j+1][1], matrixv4[i][j+1][2])
    #         glEnd()
    # end of complex shaft

    # simpler shaft
    glColor3ub(122, 24, 60)
    for i in range(0, N):
        for j in range(0, N):
            if (i < 40):
                glColor4ub(200, 130, 122, 255)
            else:
                glColor3ub(122, 24, 60)

            glBegin(GL_TRIANGLES)
            glVertex3f(matrixv5[i][j][0], matrixv5[i][j][1], matrixv5[i][j][2])
            glVertex3f(matrixv5[i+1][j][0], matrixv5[i+1][j][1], matrixv5[i+1][j][2])
            glVertex3f(matrixv5[i][j+1][0], matrixv5[i][j+1][1], matrixv5[i][j+1][2])

            glVertex3f(matrixv5[i+1][j+1][0], matrixv5[i+1]
                       [j+1][1], matrixv5[i+1][j+1][2])
            glVertex3f(matrixv5[i+1][j][0], matrixv5[i+1][j][1], matrixv5[i+1][j][2])
            glVertex3f(matrixv5[i][j+1][0], matrixv5[i][j+1][1], matrixv5[i][j+1][2])
            glEnd()

def render(time):

    # mechanizm bufora głębi
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180/3.1415/4)
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

    window = glfwCreateWindow(2000, 1000, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    matrixValues()
    matrixValuesv2()
    matrixValuesv3()
    matrixValuesv4()
    matrixValuesv5()

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
