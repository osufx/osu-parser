from osu_parser import mathhelper, curves

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
            self.curve_points = [mathhelper.Vec2(self.x, self.y)] + curve_points
            self.repeat = repeat
            self.pixel_length = pixel_length

            #For slider tick calculations
            self.timing_point = timing_point
            self.difficulty = difficulty

            self.calc_slider()
    
    def calc_slider(self):
        if self.slider_type == "P" and len(self.curve_points) > 3:
            self.slider_type = "B"
        elif len(self.curve_points) == 2:
            self.end = mathhelper.point_on_line(self.curve_points[0], self.curve_points[1], self.pixel_length)


        #Make path
        if self.slider_type == "L":     #Linear
            path = curves.Linear(self.curve_points).pos
        elif self.slider_type == "P":   #Perfect
            curve = curves.Perfect(self.curve_points)
            path = []
            l = 0
            step = 0.5
            while l <= self.pixel_length:
                path.append(curve.point_at_distance(l))
                l += step
        elif self.slider_type == "B":   #Bezier
            curve = curves.Bezier(self.curve_points, True)
            path = curve.pos
        elif self.slider_type == "C":   #Catmull
            curve = curves.Catmull(self.curve_points)
            path = curve.pos
        else:
            raise Exception("Slidertype not supported! ({})".format(self.slider_type))

        #Make end
        if not hasattr(self, 'end'):
            if self.slider_type == "L":     #Linear
                self.end = mathhelper.point_on_line(path[0], path[1], self.pixel_length)
            elif self.slider_type == "P":   #Perfect
                self.end = curve.point_at_distance(self.pixel_length)
            elif self.slider_type == "B":   #Bezier
                self.end = curve.point_at_distance(self.pixel_length)
            elif self.slider_type == "C":   #Catmull
                self.end = curve.point_at_distance(self.pixel_length)
            else:
                raise Exception("Slidertype not supported! ({})".format(self.slider_type))

        self.path = path

        #Place slider_ticks

        #Place end_point
