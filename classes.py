class Student:
    def __init__(self, name, level, taken_courses, major, gpa):
        self.name = name
        self.level = level
        self.taken_courses = taken_courses
        self.major = major
        self.gpa = gpa

class Course:
    def __init__(self, name, code, syllabus, prerequisites):
        self.name = name
        self.code = code
        self.syllabus = syllabus
        self.prerequisites = prerequisites