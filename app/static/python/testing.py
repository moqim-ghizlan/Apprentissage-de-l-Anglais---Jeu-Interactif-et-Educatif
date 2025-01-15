###################################################
def get_list_classes():
    return [c1, c2, c3, c4, c5, c6]
class Class:
    def __init__(self,id,  year, group, teachers):
        self.id = id
        self.year = year
        self.group = group
        self.teachers = teachers
c1 = Class(1, 1, "11", "JACOB")
c2 = Class(2, 1, "12", "JACOB")
c3 = Class(3, 2 , "21", "JACOB")
c4 = Class(4, 2, "22", "JACOB")
c5 = Class(5, 3, "31", "JACOB")
c6 = Class(6, 3, "32", "JACOB")
#####################################################



###################################################
def get_teachers_list():
    return [t1, t2, t3, t4, t5, t6]
class Teacher:
    def __init__(self, id,  fname, lname, email):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.email = email
t1 = Teacher(1, "JACOB","LE FORESTIER" , "jacob.le-forestier@univ-orleans.fr")
t2 = Teacher(2, "JACOB","LE FORESTIER" , "jacob.le-forestier@univ-orleans.fr")
t3 = Teacher(3, "JACOB","LE FORESTIER" , "jacob.le-forestier@univ-orleans.fr")
t4 = Teacher(4, "JACOB","LE FORESTIER" , "jacob.le-forestier@univ-orleans.fr")
t5 = Teacher(5, "JACOB","LE FORESTIER" , "jacob.le-forestier@univ-orleans.fr")
t6 = Teacher(6, "JACOB","LE FORESTIER" , "jacob.le-forestier@univ-orleans.fr")
#####################################################
###################################################
class Student:
    def __init__(self, id,  full_name, email, password, year, group):
        self.id = id
        self.full_name = full_name
        self.email = email
        self.password = password
        self.year = year
        self.group = group
s1 = Student(1, "Louis Vuitton", "louis.vuitton@etud.univ-orleans.fr", "dfsikbsqgfdbidsgrf", 1, "34")
s2 = Student(2, "john michael", "john michael@etud.univ-orleans.fr", "sdjbfvwsiudgbwuisd", 2, "11")
def get_students_list():
    return [s1, s2]
#####################################################



