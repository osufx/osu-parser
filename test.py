from osu_parser.beatmap import Beatmap


"""
Old file used to debug and check if stuff was working.
"""

beatmap = Beatmap("DEBUG.osu")
print("[DEBUG] hit_object_count: {}, max_combo: {}".format(len(beatmap.hitobjects), beatmap.max_combo))