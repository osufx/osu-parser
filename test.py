from osu_parser.beatmap import Beatmap

beatmap = Beatmap("test.osu")

print("hit_object_count: {}".format(len(beatmap.hitobjects)))