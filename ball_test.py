import sys
import turtle

snake = turtle.shape("circle")
turtle.penup()

t = 0
g = -10
b = 0.2
x, y = 0, 0
Vx, Vy = 3, 3
xlimit, ylimit = turtle.window_width() / 2.5, turtle.window_height() / 2.5

def move():
    global x, y, Vx, Vy, g

    x = x + Vx
    if -(ylimit*0.95) < y < (ylimit*0.95):
        Vy = Vy + g/2 - b*Vy
    y = y + Vy

    if not -xlimit < x < xlimit:
        Vx = -Vx
    if not -ylimit < y < ylimit:
        Vy = -Vy

    turtle.goto(x, y)

    turtle.ontimer(move, 1)

turtle.ontimer(move, 1)

def callback(event):
    print "clicked at", event.x, event.y

canvas = turtle.getcanvas()
canvas.bind('<Button-1>', callback)


#turtle.exitonclick()
turtle.done()