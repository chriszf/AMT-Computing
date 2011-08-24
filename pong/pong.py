#!/usr/bin/env python

import pyglet
from pyglet.window import key

MARGIN = 30

window = pyglet.window.Window()

X_CENTER = window.width//2
Y_CENTER = window.height//2

paddle = pyglet.resource.image("paddle.png")

paddle.anchor_x = paddle.width//2
paddle.anchor_y = paddle.height//2

LEFT_PADDLE_Y = Y_CENTER
RIGHT_PADDLE_Y = Y_CENTER

KEY_A = False
KEY_Q = False
KEY_DOWN = False
KEY_UP = False


label = pyglet.text.Label("Hello world", font_name = "Times New Roman", font_size=36,
        x = window.width//2, y = window.height//2,
        anchor_x = 'right', anchor_y = 'bottom')

@window.event
def on_key_press(symbol, modifiers):
    global KEY_A, KEY_Q, KEY_DOWN, KEY_UP, LEFT_PADDLE_Y, RIGHT_PADDLE_Y

    if symbol == key.A:
        KEY_A = True
    elif symbol == key.Q:
        KEY_Q = True
    elif symbol == key.UP:
        KEY_UP = True
    elif symbol == key.DOWN:
        KEY_DOWN = True
    elif symbol == key.ESCAPE:
        pass

    print "PRESS", symbol

@window.event
def on_key_release(symbol, modifiers):
    global KEY_A, KEY_Q, KEY_DOWN, KEY_UP, LEFT_PADDLE_Y, RIGHT_PADDLE_Y

    if symbol == key.A:
        KEY_A = False
    elif symbol == key.Q:
        KEY_Q = False
    elif symbol == key.UP:
        KEY_UP = False
    elif symbol == key.DOWN:
        KEY_DOWN = False
    elif symbol == key.ESCAPE:
        pass

    print "RELEASE", symbol

@window.event
def on_draw():
    window.clear()
    global LEFT_PADDLE_Y, RIGHT_PADDLE_Y

    if KEY_A == True:
        LEFT_PADDLE_Y -= 5
    elif KEY_Q == True:
        LEFT_PADDLE_Y += 5

    if KEY_UP == True:
        RIGHT_PADDLE_Y += 5
    elif KEY_DOWN == True:
        RIGHT_PADDLE_Y -= 5

    # Left paddle
    paddle.blit(MARGIN, LEFT_PADDLE_Y)

    # Right paddle
    paddle.blit(window.width-MARGIN, RIGHT_PADDLE_Y)

    # Dividing line
#    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
#            ('v2i', (X_CENTER, MARGIN, X_CENTER, window.height-MARGIN)),
#            ('c3B', (0, 0, 255, 255, 255, 0))
#            )



pyglet.app.run()
