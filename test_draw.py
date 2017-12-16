import turtle
import time
from osu_parser.beatmap import Beatmap

beatmap = Beatmap("DEBUG.osu")

wn = turtle.Screen()
tur = turtle.Turtle()
tur.penup()
tur.speed(1)

for hitobject in beatmap.hitobjects:
    #if hitobject.time < 8000:
        #continue
    tur.goto(hitobject.x, -hitobject.y)
    tur.pendown()
    tur.pencolor("red")
    if 2 & hitobject.type:
        tur.dot(6)
        #for point in hitobject.path:
            #tur.goto(point.x, -point.y)
            #time.sleep(0.1)
        print("time: {}, x: {}, y: {}, type: sliderStart, duration: {}".format(hitobject.time, hitobject.x, hitobject.y, hitobject.duration))
        
        i = 0
        for tick in hitobject.ticks:
            tur.goto(tick.x, -tick.y)
            print("time: {}, x: {}, y: {}, type: tick, num: {}".format(tick.time, tick.x, tick.y, i))
            time.sleep(1.5)
            i += 1
            tur.dot(6, "black")

        i = 0
        for end_tick in hitobject.end_ticks:
            tur.goto(end_tick.x, -end_tick.y)
            print("time: {}, x: {}, y: {}, type: end_tick, num: {}".format(end_tick.time, end_tick.x, end_tick.y, i))
            time.sleep(1.5)
            i += 1
            tur.dot(6, "gray")
    else:
        tur.pencolor("blue")
        tur.dot(6)
        print("time: {}, x: {}, y: {}, type: hitCircle".format(hitobject.time, hitobject.x, hitobject.y))
    tur.penup()

wn.exitonclick()