from turtle import *
from osu_parser.beatmap import Beatmap

beatmap = Beatmap("test.osu")

for hitobject in beatmap.hitobjects:
    plot.scatter(hitobject.x,hitobject.y)

pyplot.show()