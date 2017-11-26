import math
from osu_parser import mathhelper, curves

class SliderTick(object):
    def __init__(self, x, y, time):
        self.x = x
        self.y = y
        self.time = time

class HitObject(object):
    def __init__(self, x, y, time, object_type, slider_type = None, curve_points = None, repeat = 1, pixel_length = 0, timing_point = None, px_per_beat = 1, difficulty = None, tick_distance = 1):
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
        px_per_beat -- pixels per. beat
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
            self.px_per_beat = px_per_beat
            self.difficulty = difficulty
            self.tick_distance = tick_distance

            self.ticks = []

            self.calc_slider(True)
    
    def calc_slider(self, calc_path = False):
        num_beats = (self.pixel_length * self.repeat) / self.px_per_beat
        self.duration = math.ceil(num_beats * self.timing_point["mpb"])

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

        #End time
        self.end_time = self.time + self.duration

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
        
        #Put end time on end point
        self.end = SliderTick(self.end.x, self.end.y, self.end_time)

        #Quick calc how many ticks
        self.object_count = (math.ceil((num_beats - 0.1) / self.repeat * self.difficulty["SliderTickRate"]) - 1) * self.repeat + self.repeat + 1

        #Set slider ticks
        #tick_distance = (self.timing_point["spm"] * self.timing_point["mpb"]) / self.px_per_beat
        #tick_distance = (100 * self.difficulty["SliderMultiplier"]) / self.difficulty["SliderTickRate"]

        

        print("spm: {}, mpb: {}, px_per_beat: {}, tick_distance: {}".format(self.timing_point["spm"], self.timing_point["mpb"], self.px_per_beat, self.tick_distance))
        current_distance = self.tick_distance
        time_add = self.duration / self.object_count
        while current_distance < self.pixel_length - 1:
            if self.slider_type == "L":     #Linear
                point = mathhelper.point_on_line(self.curve_points[0], self.curve_points[1], current_distance)
            else:   #Perfect, Bezier & Catmull uses the same function
                point = curve.point_at_distance(current_distance)
            self.ticks.append(SliderTick(point.x, point.y, self.time + time_add * (len(self.ticks) + 1)))
            current_distance += self.tick_distance

        """
        current_time = self.time + self.px_per_beat
        while current_time < self.end_time:
            dist = 
            current_time += self.px_per_beat
        """
            
        """
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
        """