# ------------------------------------------------------------------------------------------
# Title: Assignment07
# Desc: This assignment demonstrates how to use functions and classes
# Change Log: (Who, When, What)
#   Abarna,2/24/2024, Created Script
# ------------------------------------------------------------------------------
import json
import sys
from typing import IO
from json import JSONDecodeError

# creating a constant for a course registration program
MENU: str = """
----Course Registration Program----
Select from the following menu
1. Register a student for a course
2. Show current data
3. Save data to the file
4. Exit the program
------------------------------------
"""
file_name: str = 'Enrollments.json'
menu_choice: str = ""
students: list = []


class FileProcessor:

    @staticmethod
    def read_data_from_file(file_name):
        """
        Reads data from file
        :param file_name:
        :return
        """
        global students
        try:
            with open(file_name, "r") as file:
                data = json.load(file)
                students = [Student(item['first_name'], item['last_name'], item['course_name']) for item in data]
                for student in students:
                    print(f"{student.first_name} {student.last_name} for {student.course_name}")
        except FileNotFoundError as error:
            IO.output_error_messages("File Not Found", error)
            print("Creating a new file")
            with open(file_name, "w") as file:
                json.dump(students, file)
        except JSONDecodeError as error:
            IO.output_error_messages("Invalid JSON file", error)
            print("Creating a new file")
            with open(file_name, "w") as file:
                json.dump(students, file)
        except Exception as error:
            print(error)
            IO.output_error_messages("unhandled exception", error)
        return students

    @staticmethod
    def write_data_to_file(file_name, students):
        """
        writes data to file
        :param file_name:
        :param students:
        :return:
        """
        try:
            with open(file_name, "w") as file:
                students_dict = [student.to_dict() for student in students]
                json.dump(students_dict, file)
                for student in students:
                    print(f"You have registered {student.first_name} {student.last_name} for {student.course_name}")
        except ValueError as error:
            IO.output_error_messages("Unhandled exception ", error)
        except Exception as error:
            IO.output_error_messages("There was an error writing to the file", error)


class IO:
    global students

    @staticmethod
    def output_error_messages(message, error: Exception = None):
        """
        displays the error messages
        :param message:
        :param error:
        """
        print(message)
        if error is not None:
            print("---Technical Information---")
            print(error, error.__doc__)

    def output_menu(self):
        pass

    @staticmethod
    def input_menu_choice(menu):
        print(menu)
        choice = input("What would you like to do: ")
        return choice

    @staticmethod
    def input_student_data(students):
        """
        Function to get input from the user
        :param Students
        :return: updated student data
        """
        try:
            student_first_name = input("Enter student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("First name must contain only alphabets")
            student_last_name = input("Enter student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("Last name must contain only alphabets")
            course_name = input("Enter course name: ")
            student = Student(student_first_name, student_last_name, course_name)
            students.append(student)
        except ValueError as e:
            IO.output_error_messages("User entered invalid name")
        except Exception as e:
            IO.output_error_messages("Unhandled exception", e)
        finally:
            return students

    @staticmethod
    def output_student_data(students):
        try:
            for student in students:
                print(f"{student.first_name} {student.last_name} registered for {student.course_name}")
        except Exception as e:
            IO.output_error_messages("unhandled exception", e)


class Person:
    _first_name: str = ""
    _last_name: str = ""

    def __init__(self, first_name, last_name):
        """
        Constructor to initialize a Person object
        :param first_name:
        :param last_name:
        """
        self._first_name = first_name
        self._last_name = last_name

    @property
    def first_name(self):
        """
        Returns the first name of the person
        """
        return self._first_name.title()

    @first_name.setter
    def first_name(self, first_name):
        """
        Sets the first name of the person
        :param first_name
        """
        if first_name.isalpha():
            self._first_name = first_name.title()
        else:
            IO.output_error_messages("First name must contain only alphabets")

    @property
    def last_name(self):
        """
        Returns the last name of the person
        """
        return self._last_name.title()

    @last_name.setter
    def last_name(self, last_name):
        """
        Sets the last name of the person
        :param last_name
        """
        if last_name.isalpha():
            self._last_name = last_name.title()
        else:
            IO.output_error_messages("Last name must contain only alphabets")

    def __str__(self):
        """
        Returns the string representation of the person object
        :return:
        """
        return f"{self._first_name} {self._last_name}"


class Student(Person):
    """
    A student class that inherits properties from Person class
    """
    course_name: str = ""

    def __init__(self, first_name, last_name, course_name):
        """
        constructor to initialize the student object
        :param first_name
        :param last_name
        :param course_name
        """
        super().__init__(first_name, last_name)
        self.course_name = course_name

    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'course_name': self.course_name
        }

    def __str__(self):
        """
        Returns the string representation of the Student object
        :return:
        """
        return f"{self.first_name} {self.last_name} {self.course_name}"


students: list = FileProcessor.read_data_from_file(file_name)
while True:
    choice = IO.input_menu_choice(MENU)
    if choice == "1":
        students = IO.input_student_data(students)
    elif choice == "2":
        IO.output_student_data(students)
    elif choice == "3":
        FileProcessor.write_data_to_file(file_name, students)
    elif choice == "4":
        sys.exit()
    else:
        print("Invalid choice. Please enter a valid choice")
