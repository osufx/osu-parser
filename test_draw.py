import turtle
from osu_parser.beatmap import Beatmap

beatmap = Beatmap("test.osu")

wn = turtle.Screen()
tur = turtle.Turtle()
tur.penup()
tur.speed(8)

for hitobject in beatmap.hitobjects:
    print(hitobject.time)
    if hitobject.time != 26125:
        continue
    tur.goto(hitobject.x, -hitobject.y)
    tur.pendown()
    tur.pencolor("red")
    if 2 & hitobject.type:
        tur.dot(6)
        for point in hitobject.path:
            tur.goto(point.x, -point.y)
        print(hitobject.end)
        tur.goto(hitobject.end.x, -hitobject.end.y)
        tur.pencolor("green")
        tur.dot(6)

        tur.penup()
        
        for tick in hitobject.ticks:
            tur.goto(tick.x, -tick.y)
            tur.dot(6, "black")

    else:
        tur.pencolor("blue")
        tur.dot(6)
    tur.penup()

wn.exitonclick()