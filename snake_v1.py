import sys
import turtle

wn = turtle.Screen()
wn.bgcolor('lightblue')

snake = turtle.shape("circle")
turtle.pensize(10)
turtle.penup()

cherry = 10
t = 0
x, y = 0, 0
Vsnake = 10
xlimit, ylimit = turtle.window_width() / 2.5, turtle.window_height() / 2.5

def move():
    global x, y, Vsnake, t, cherry
    t = t + 1
    turtle.forward(Vsnake)
    turtle.stamp();

    if cherry > 0:
        cherry = cherry - 1
    else:
        turtle.clearstamps(1)


    turtle.ontimer(move, 100)
turtle.ontimer(move, 100)

def callback(event):
    global cherry
    print event.x, event.y
    #cherry = 1


canvas = turtle.getcanvas()
canvas.bind('<Button-1>', callback)

wn.onkey(lambda: turtle.setheading(90), 'Up')
wn.onkey(lambda: turtle.setheading(180), 'Left')
wn.onkey(lambda: turtle.setheading(0), 'Right')
wn.onkey(lambda: turtle.setheading(270), 'Down')
wn.listen()


#turtle.exitonclick()
turtle.done()