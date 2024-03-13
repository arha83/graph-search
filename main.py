import cv2 as cv
import numpy as np
from graph import *
from drawing import *

windowWidth= 800
windowHeight= 600

v= [*'abcdefgh']
e= [('h', 'b', 2), ('h', 'd', 3), ('h', 'c', 3), ('h', 'f', 3),
    ('b', 'c', 3),
    ('d', 'b', 4), ('d', 'c', 4),
    ('c', 'f', 3),
    ('f', 'a', 3), ('f', 'e', 3),
    ('a', 'e', 3),
    ('e', 'g', 3)]
h={
    'h': 5,
    'd': 5,
    'b': 2,
    'c': 4,
    'f': 5,
    'a': 5,
    'e': 3,
    'g': 0,
}
np.random.shuffle(v)
np.random.shuffle(e)
# v= [*'abcdefgh']
# e= [
#     ('a','b',1),('a','c',1),('a','d',1),
#     ('b','a',1),('b','c',1),('b','d',1),
#     ('c','a',1),('c','b',1),('c','d',1),
#     ('d','a',1),('d','b',1),('d','c',1),('d','f',3),
#     ('e','f',1),('e','g',1),('e','h',1),
#     ('f','e',1),('f','g',1),('f','h',1),
#     ('g','e',1),('g','f',1),('g','h',1),
#     ('h','e',1),('h','f',1),('h','g',1),
# ]
np.random.shuffle(v)
np.random.shuffle(e)
g= Graph(v, e)
gd= GraphDrawer(g, windowWidth, windowHeight)

canvas= np.zeros((windowHeight, windowWidth, 3), np.uint8)
gd.draw(canvas)
cv.imshow('Pleeeaaaase work :(', canvas)
cv.waitKey()
cv.waitKey(500)

for i in range(2000):
    canvas= np.zeros((windowHeight, windowWidth, 3), np.uint8)
    gd.draw(canvas)
    gd.update(iterations= 5)
    cv.imshow('Pleeeaaaase work :(', canvas)
    if cv.waitKey(1) == ord('q'): break

for path in g.uniformCostSearch_yield('h', 'g'):
    canvas= np.zeros((windowHeight, windowWidth, 3), np.uint8)
    cv.putText(canvas, 'Uniform Cost Search', (2,20), cv.FONT_HERSHEY_COMPLEX, 0.7, (255,255,0))
    gd.draw(canvas, path)
    cv.imshow('Pleeeaaaase work :(', canvas)
    if cv.waitKey(250) == ord('q'): break

cv.waitKey(2000)

for path in g.breadthFirstSearch_yield('h', 'g'):
    canvas= np.zeros((windowHeight, windowWidth, 3), np.uint8)
    cv.putText(canvas, 'Breadth First Search', (2,20), cv.FONT_HERSHEY_COMPLEX, 0.7, (255,255,0))
    gd.draw(canvas, path)
    cv.imshow('Pleeeaaaase work :(', canvas)
    if cv.waitKey(250) == ord('q'): break

cv.waitKey(2000)

for path in g.depthFirstSearch_yield('h', 'g'):
    canvas= np.zeros((windowHeight, windowWidth, 3), np.uint8)
    cv.putText(canvas, 'Depth First Search', (2,20), cv.FONT_HERSHEY_COMPLEX, 0.7, (255,255,0))
    gd.draw(canvas, path)
    cv.imshow('Pleeeaaaase work :(', canvas)
    if cv.waitKey(250) == ord('q'): break

cv.waitKey(2000)

for path in g.AStarSearch_yield('h', 'g', h):
    canvas= np.zeros((windowHeight, windowWidth, 3), np.uint8)
    cv.putText(canvas, 'A* Search', (2,20), cv.FONT_HERSHEY_COMPLEX, 0.7, (255,255,0))
    gd.draw(canvas, path)
    cv.imshow('Pleeeaaaase work :(', canvas)
    if cv.waitKey(250) == ord('q'): break

cv.waitKey(2000)


cv.destroyAllWindows()


