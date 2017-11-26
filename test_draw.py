import turtle
from osu_parser.beatmap import Beatmap

beatmap = Beatmap("test.osu")

wn = turtle.Screen()
tur = turtle.Turtle()
tur.penup()
tur.speed(8)

for hitobject in beatmap.hitobjects:
    if hitobject.time < 36300 or hitobject.time > 37600:
        continue
    print(hitobject.time)
    tur.goto(hitobject.x, -hitobject.y)
    tur.pendown()
    tur.pencolor("red")
    if 2 & hitobject.type:
        tur.dot(6)
        for point in hitobject.path:
            tur.goto(point.x, -point.y)
        print("start: {}, end: {}, duration: {}".format(hitobject.time, hitobject.end_time, hitobject.duration))
        tur.goto(hitobject.end.x, -hitobject.end.y)
        tur.pencolor("green")
        tur.dot(6)

        tur.penup()
        
        i = 0
        for tick in hitobject.ticks:
            tur.goto(tick.x, -tick.y)
            print("id: {}, time: {}".format(i, tick.time))
            i += 1
            #print("time: {}, pos: {}".format(hitobject.time, "(X:{} Y:{})".format(tick.x, tick.y)))
            tur.dot(6, "black")

    else:
        tur.pencolor("blue")
        tur.dot(6)
    tur.penup()

wn.exitonclick()