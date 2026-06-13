class Person():
    def get_details(self):
        return "Details of a person."
    
    def test_mro(self):
        return "Person is tesing MRO"


class Athlete():
    def get_skill(self):
        return "Athletic skills."
    
    def test_mro(self):
        return "Athlete is tesing MRO...or not?"


class Student(Person, Athlete):
    pass


student = Student()
print(student.get_details())
print(student.get_skill())

print(Student.__mro__)

print(student.test_mro())