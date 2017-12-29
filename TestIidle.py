class Student(object):
    def __init__(self,name,score):
        self.name = name
        self.score = score

bart = Student('我的',90)
print(bart.name)
print(bart.score)