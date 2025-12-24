"""
To-Do:
-update student avg
- fix course student list
"""


def initialize_school(filename: str, lst1: list, lst2: list, dict1: dict):
	with open(filename, "r") as file:
		data = file.read()
		for line in data.split('\n'):
			if line == "":
				continue
			
			s_info = line.split(',')
			

			if s_info[0] == "Student":
				name, id, age = s_info[1], int(s_info[2]), s_info[3]
				s = Student(name, id, age)
				lst1.append(s)
			elif s_info[0] == "Course":
				code, credits = s_info[1], s_info[2]
				c = Course(code, credits)
				if c not in lst2:
					lst2.append(c)
			elif s_info[0] == "Curriculum":
				cur_name = s_info[1].strip()
				cur_courses = [course.strip() for course in s_info[2].split(";")]
				dict1[cur_name] = cur_courses




def print_school(s_list, c_list):
	for s in s_list:
		print(s)
	print()
	for c in c_list:
		print(c)



class School:
	def __init__(self):
		self.courses = course_list
		self.students = student_list

	def show_courses(self):
		for course in self.courses:
			print(course)
			for st in course.students:
				print("   ", st)
			print("-"*20)


class Student:
	def __init__(self, name: str, id: int, age: int, school=None):
		self.name = name
		self.id = id
		self.age = age
		self.courses = []
		self.grades = {}
		self.avg = 0
		self.school = sch
		
	def enter_grade(self, course_code: str, grade):
		if course_code not in self.grades:
			return None
		self.grades[course_code].append(grade)

	def course_avg(self, course_code):
		course_grades = self.grades[course_code]
		if len(course_grades) == 0:
			return 0
		avg = sum(course_grades) / len(course_grades)
		return round(avg)
	
	def update_avg(self):
		pass

	def enroll_class(self, code: str):
		for course in self.school.courses:
			if course.code == code:
				if self not in course.students:
					course.students.append(self)
					self.courses.append(course.code)

				if code not in self.grades:
					self.grades[code] = []
				return
			

	def enroll_to_department(self, dep: str):
		for course in self.school.courses:
			data = course.code.split("-")
			department = data[0].strip()
			if department == dep:
				self.enroll_class(course.code)

	def enroll_curriculum(self, cur: list):
		if cur not in curriculums:
			raise KeyError("Curriculum code not found")
			return
		for code in curriculums[cur]:
			self.enroll_class(code)

	def __str__(self):
		return f"Name: {self.name:8} |  ID: {self.id} "
				
				

class Course:
	def __init__(self, code: str, credits: int):
		self.code = code.strip()
		self.credits = credits
		self.students = []
		self.school = sch
		#self.add_course()

	def add_course(self):
		self.school.courses.append(self)

	def __str__(self):
		return f"{self.code:10}| {self.credits} credits"



student_list = []
course_list = []
curriculums = {}

sem_cur = ["MATH-262", "MATH-263", "MATH-240", "COMP-202"]


####these are needed to set up the school
sch = School()

initialize_school("data.csv", student_list, course_list, curriculums)
###


students = student_list[0 : 6]
for i, st in enumerate(students):
	st.enroll_curriculum("CE-SEM-1")
	if i % 2 == 0:
		st.enroll_curriculum("CE-SEM-2")
	elif i == 3:
		st.enroll_class('MATH-262')
		#print(st.grades)


#sch.show_courses()

def main():
	print(" ---LOGIN---")
	valid_status = False
	while not valid_status:
		status = input("Student (S) or Staff (F): ")
		if status == "S" or status == "F":
			valid_status = True
		else:
			print("Invalid entry")
	if status == "S":
		while True:
			student_id = int(input("Enter Student ID: "))
			student = find_id(student_id)
			if student:
				break
			print("Unknown ID")
		print(student)


def find_id(id: int):
	for st in student_list:
		if st.id == id:
			return st
	return None




if __name__ == "__main__":
	main()
			





#print(curriculums)




# # print_school(student_list, course_list)
# s1 = student_list[9]
# s2 = student_list[8]
# s1.enroll_curriculum(sem_cur)
# s1.enroll_class("MATH-262")
# s2.enroll_to_department("MATH")
# print(s2.courses)
# #print(s1.grades)
# #print(s1.grades)
# c1 = course_list[1]
# #print(c1)
# # print(f"{c1.code} Students")
# # for st in c1.students:
# # 	print(st)


