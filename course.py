# Joey Rudek, @jrdek, jer5ae
# October 21, 2019

class DictClass:
    def __init__(self, d):
        for key in d:
            setattr(self,key,d[key])

class Instructor(DictClass):
    pass

class Meeting_Pattern(DictClass):
    pass

class Course(DictClass):
    def __init__(self, result):
        super().__init__(result)
        self.instructors = [Instructor(d) for d in result["instructors"]]
        self.class_meeting_patterns = [Meeting_Pattern(d) for d in result["class_meeting_patterns"]]
