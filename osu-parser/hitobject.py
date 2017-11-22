class HitObject(object):
    def __init__(self, x, y, time, object_type, slider_type = None, curve_points = None, repeat = 1, pixel_length = 0, timing_point = None, difficulty = None):
        """
        HitObject params for normal hitobject and sliders

        x -- x position
        y -- y position
        time -- timestamp
        object_type -- type of object (bitmask)

        [+] IF SLIDER
        slider_type -- type of slider (L, P, B, C)
        curve_points -- points in the curve path
        repeat -- amount of repeats for the slider (+1)
        pixel_length -- length of the slider
        timing_point -- ref of current timing point for the timestamp
        difficulty -- ref of beatmap's difficulty
        """
        self.x = x
        self.y = y
        self.time = time
        self.type = object_type

        #isSlider?
        if 2 & self.type:
            self.slider_type = slider_type
            self.curve_points = curve_points
            self.repeat = repeat
            self.pixel_length = pixel_length
            self.timing_point = timing_point
            self.difficulty = difficulty

