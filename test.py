from osu_parser.beatmap import Beatmap

beatmap = Beatmap("reanimate.osu")

print("hit_object_count: {}, max_combo: {}".format(len(beatmap.hitobjects), beatmap.max_combo))