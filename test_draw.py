import turtle
from osu_parser.beatmap import Beatmap

beatmap = Beatmap("test.osu")

wn = turtle.Screen()
tur = turtle.Turtle()
tur.penup()
tur.speed(10)

for hitobject in beatmap.hitobjects:
    if hitobject.time < 396203:
        continue
    tur.goto(hitobject.x, -hitobject.y)
    tur.pendown()
    tur.pencolor("red")
    if 2 & hitobject.type:
        tur.dot(6)
        for point in hitobject.path:
            tur.goto(point.x, -point.y)
    else:
        tur.pencolor("blue")
        tur.dot(6)
    tur.penup()

wn.exitonclick()