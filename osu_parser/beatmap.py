from osu_parser import mathhelper
from osu_parser.hitobject import HitObject

class Beatmap(object):
    """
    Beatmap object for beatmap parsing and handling
    """

    def __init__(self, file_name):
        """
        file_name -- Directory for beatmap file (.osu)
        """
        self.file_name = file_name
        self.header = -1
        self.difficulty = {}
        self.timing_points = {
            "mpb": {},  #Raw code
            "bpm": {},  #Beats pr minute
            "spm": {}   #Speed modifier
        }
        self.hitobjects = []
        self.parse_beatmap()
        #self.object_count = self.get_object_count()
    
    def parse_beatmap(self):
        """
        Parses beatmap file line by line by passing each line into parse_line.
        """
        with open(self.file_name) as file_stream:
            for line in file_stream:
                self.parse_line(line.replace("\n", ""))

    def parse_line(self, line):
        """
        Parse a beatmapfile line.

        Handles lines that are required for our use case (Difficulty, TimingPoints & hitobjects), 
        everything else is skipped.
        """
        if len(line) < 1:
            return

        if line.startswith("["):
            if line == "[Difficulty]":
                self.header = 0
            elif line == "[TimingPoints]":
                self.header = 1
            elif line == "[HitObjects]":
                self.header = 2
            else:
                self.header = -1
            return

        if self.header == -1: #We return if we are reading under a header we dont care about
            return

        if self.header == 0:
            self.handle_difficulty_propperty(line)
        elif self.header == 1:
            self.handle_timing_point(line)
        elif self.header == 2:
            self.handle_hitobject(line)
    
    def handle_difficulty_propperty(self, propperty):
        """
        Puts the [Difficulty] propperty into the difficulty dict.
        """
        prop = propperty.split(":")
        self.difficulty[prop[0]] = float(prop[1])

    def handle_timing_point(self, timing_point):
        """
        Formats timing points used for slider velocity changes,
        and store them into self.timing_points dict.
        """
        timing_point_split = timing_point.split(",")
        timing_point_time = int(timing_point_split[0])
        timing_point_focus = timing_point_split[1]

        if timing_point_focus.startswith("-"):  #If not then its not a slider velocity modifier
            self.timing_points["spm"][timing_point_time] = -100 / float(timing_point_focus) #Convert to normalized value and store
        else:
            self.timing_points["bpm"][timing_point_time] = 60000 / float(timing_point_focus)#^
            self.timing_points["mpb"][timing_point_time] = float(timing_point_focus)        #We use this value to modify slider velocity_red

    def handle_hitobject(self, line):
        """
        Puts every hitobject into the hitobjects array.

        Creates hitobjects, hitobject_sliders or skip depending on the given data.
        We skip everything that is not important for us for our use case (Spinners)
        """
        split_object = line.split(",")
        time = int(split_object[2])
        object_type = int(split_object[3])

        if not (1 & object_type > 0 or 2 & object_type > 0):  #We only want sliders and circles as spinners are random bannanas etc.
            return

        if 2 & object_type:  #Slider
            time_point = self.get_timing_point_all(time)

            curve_split = split_object[5].split("|")
            curve_points = []
            for i in range(1, len(curve_split)):
                vector_split = curve_split[i].split(":")
                vector = mathhelper.Vec2(int(vector_split[0]), int(vector_split[1]))
                curve_points.append(vector)
            hitobject = HitObject(int(split_object[0]), int(split_object[1]), time, object_type, curve_split[0], curve_points, int(split_object[6]), float(split_object[7]), time_point, self.difficulty)
        else:
            hitobject = HitObject(int(split_object[0]), int(split_object[1]), time, object_type)

        self.hitobjects.append(hitobject)

    def get_timing_point_all(self, time):
        """
        Returns a object of all current timing types

        time -- timestamp
        return -- {"mpb": Float, "bpm": Float, "spm": Float}
        """
        types = {
            "mpb": 100,
            "bpm": 100,
            "spm": 1
        }   #Will return the default value if timing point were not found
        for t in types.keys():
            r = self.get_timing_point(time, t)
            if r > 0:
                types[t] = r
            else:
                print("{} were not found for timestamp {}, using {} instead.".format(t, time, types[t]))

        return types

    def get_timing_point(self, time, timing_type):
        """
        Returns latest timing point by timestamp (Current)

        time -- timestamp
        timing_type -- mpb, bmp or spm
        return -- self.timing_points object
        """
        r = -1
        for key in self.timing_points[timing_type].keys():
            if key <= time:
                r = self.timing_points[timing_type][key]
            else:
                break
        return r

    def get_object_count(self):
        """
        Get the total hitobject count for the parsed beatmap (Normal hitobjects, sliders & sliderticks)

        return -- total hitobjects for parsed beatmap
        """
        count = 0
        for hitobject in self.hitobjects:
            count += hitobject.get_points()
        return count
