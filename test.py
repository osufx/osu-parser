from osu_parser.beatmap import Beatmap


"""
Old file used to debug and check if stuff was working.
"""

beatmap = Beatmap("slider_types.osu")
print("[slider_types] hit_object_count: {}, max_combo: {}".format(len(beatmap.hitobjects), beatmap.max_combo))

beatmap = Beatmap("v14.osu")
print("[v14] hit_object_count: {}, max_combo: {}".format(len(beatmap.hitobjects), beatmap.max_combo))

beatmap = Beatmap("v11.osu")
print("[v11] hit_object_count: {}, max_combo: {}".format(len(beatmap.hitobjects), beatmap.max_combo))
2070

beatmap = Beatmap("v14_2.osu")
print("[v14_2] hit_object_count: {}, max_combo: {}".format(len(beatmap.hitobjects), beatmap.max_combo))

beatmap = Beatmap("v11_2.osu")
print("[v11_2] hit_object_count: {}, max_combo: {}".format(len(beatmap.hitobjects), beatmap.max_combo))


beatmap = Beatmap("DEBUG.osu")
print("[DEBUG] hit_object_count: {}, max_combo: {}".format(len(beatmap.hitobjects), beatmap.max_combo))