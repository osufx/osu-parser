import turtle
from osu_parser.beatmap import Beatmap

beatmap = Beatmap("test.osu")

wn = turtle.Screen()
tur = turtle.Turtle()
tur.penup()
tur.speed(10)

for hitobject in beatmap.hitobjects:
    tur.goto(hitobject.x, -hitobject.y)
    tur.pendown()
    tur.pencolor("red")
    if 2 & hitobject.type:
        for point in hitobject.path:
            tur.goto(point.x, -point.y)
    else:
        tur.pencolor("blue")
        tur.forward(2)
    tur.penup()

wn.exitonclick()