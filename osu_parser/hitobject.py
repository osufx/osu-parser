from osu_parser import mathhelper, curves

class SliderTick(object):
    def __init__(self, x, y, time):
        self.x = x
        self.y = y
        self.time = time

class HitObject(object):
    def __init__(self, x, y, time, object_type, slider_type = None, curve_points = None, repeat = 1, pixel_length = 0, timing_point = None, tick_distance = 1):
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
        tick_distance -- distance betwin slider ticks
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
            self.tick_distance = tick_distance * self.timing_point["spm"] * 1000

            self.ticks = []

            self.calc_slider(True)
    
    def calc_slider(self, calc_path = False):
        current_distance = self.tick_distance

        #Fix broken objects
        if self.slider_type == "P" and len(self.curve_points) > 3:
            self.slider_type = "B"
        elif len(self.curve_points) == 2:
            self.slider_type = "L"

        #Make curve
        if self.slider_type == "P":     #Perfect
            curve = curves.Perfect(self.curve_points)
        elif self.slider_type == "B":   #Bezier
            curve = curves.Bezier(self.curve_points, True)
        elif self.slider_type == "C":   #Catmull
            curve = curves.Catmull(self.curve_points)

        #Quickest to skip this
        if calc_path: #Make path if requested (For drawing visual for testing)
            if self.slider_type == "L":     #Linear
                self.path = curves.Linear(self.curve_points).pos
            elif self.slider_type == "P":   #Perfect
                self.path = []
                l = 0
                step = 5
                while l <= self.pixel_length:
                    self.path.append(curve.point_at_distance(l))
                    l += step
            elif self.slider_type == "B":   #Bezier
                self.path = curve.pos
            elif self.slider_type == "C":   #Catmull
                self.path = curve.pos
            else:
                raise Exception("Slidertype not supported! ({})".format(self.slider_type))

        #End points
        if self.slider_type == "L":     #Linear
            self.end = mathhelper.point_on_line(self.curve_points[0], self.curve_points[1], self.pixel_length)
        elif self.slider_type == "P":   #Perfect
            self.end = curve.point_at_distance(self.pixel_length)
        elif self.slider_type == "B":   #Bezier
            self.end = curve.point_at_distance(self.pixel_length)
        elif self.slider_type == "C":   #Catmull
            self.end = curve.point_at_distance(self.pixel_length)
        else:
            raise Exception("Slidertype not supported! ({})".format(self.slider_type))

        print("bpm: {}".format(self.timing_point["bpm"]))

        #Set slider ticks
        if self.slider_type == "L":     #Linear
            while current_distance < self.pixel_length:
                point = mathhelper.point_on_line(self.curve_points[0], self.curve_points[1], current_distance)
                self.ticks.append(SliderTick(point.x, point.y, self.time+1))#TODO: Fix time
                current_distance += self.tick_distance
        elif self.slider_type == "P":   #Perfect
            while current_distance < self.pixel_length:
                point = curve.point_at_distance(current_distance)
                self.ticks.append(SliderTick(point.x, point.y, self.time+1))#TODO: Fix time
                current_distance += self.tick_distance
        elif self.slider_type == "B":   #Bezier
            while current_distance < self.pixel_length:
                point = curve.point_at_distance(current_distance)
                self.ticks.append(SliderTick(point.x, point.y, self.time+1))#TODO: Fix time
                current_distance += self.tick_distance
        elif self.slider_type == "C":   #Catmull
            while current_distance < self.pixel_length:
                point = curve.point_at_distance(current_distance)
                self.ticks.append(SliderTick(point.x, point.y, self.time+1))#TODO: Fix time
                current_distance += self.tick_distance