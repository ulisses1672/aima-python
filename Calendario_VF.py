import sys
sys.path.append(r'D:\_MIAA\FIA\aima-python-master')

#from csp import *
# from notebook import psource, plot_NQueens

# %matplotlib inline
# Hide warnings in the matplotlib sections

import math
import warnings
warnings.filterwarnings("ignore")
import random
from csp import CSP, min_conflicts
from collections import Counter

# Define the classes
classes = ["Math", "English", "History", "Science"]
quantity = [1, 3, 1,1]

class_info = [f"{class_name}{i+1}" for class_name, count in zip(classes, quantity) for i in range(count)]

# Define the rooms
rooms = ["Room1", "Room2", "Room3", "Room4", "Room5", "Room6", "Room7", "Room8"]

# Define the days
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Define the teachers for each class
teachers = {"Math": "Teacher1", "English": "Teacher2", "History": "Teacher3", "Science": "Teacher4"}

# Define the availability of each teacher
availability = {
    "Teacher1": [("Monday", "9AM"),("Monday", "11AM"), ("Tuesday", "1PM"), ("Tuesday", "3PM")],
    "Teacher2": [("Monday", "9AM"),("Monday", "11AM"), ("Monday", "1PM"), ("Monday", "3PM")],
    "Teacher3": [("Monday", "9AM"),("Monday", "11AM"), ("Monday", "1PM"), ("Monday", "3PM"),("Friday", "9AM"),("Friday", "11AM"), ("Friday", "1PM"), ("Friday", "3PM")],
    "Teacher4":  [("Wednesday", "9AM"),("Wednesday", "11AM"), ("Wednesday", "1PM"), ("Wednesday", "3PM"),("Thursday", "9AM"),("Thursday", "11AM"), ("Thursday", "1PM"), ("Thursday", "3PM")]
}

# Define the time slots for each day
time_slots = [(day, time) for day in days for time in ["9AM", "11AM", "1PM", "3PM", "5PM"]]

# Define the domains
index = 0
domains = {}
domainTotal = {}


for class_ in class_info:
    className= class_[:-1]
    teacher = teachers[className]
    index = index + 1
    domains[class_] = [(time_slot, room) for time_slot in time_slots[:25] if time_slot in availability[teacher] for room in rooms]     #25 slots de tempo disponiveis para cada professor

# Define the neighbors
neighbors = {class_: [other_class for other_class in class_info if other_class != class_] for class_ in class_info}


def is_teacher_available(teacher, day, time, availability):
    if teacher in availability:
        for available_day, available_time in availability[teacher]:
            if available_day == day and available_time == time:
                return True
    return False


def get_teacher_by_class(class_name, teachers):
    return teachers.get(class_name, None)

def checkQuantity(quantity):
    for value in quantity:
        if value > 2:
            return True  
    return False

    

# Define the constraints

def constraint(class_a, time_room_a, class_b, time_room_b):
    day_a, time_a = time_room_a[0]
    room_a = time_room_a[1]

    day_b, time_b = time_room_b[0]
    room_b = time_room_b[1]

    teacher_a = get_teacher_by_class(class_a[:-1], teachers)
    teacher_b = get_teacher_by_class(class_b[:-1], teachers)

    if(checkQuantity(quantity)):
        return False
    
    # Check if both time slots and rooms are available, and if teachers are available
    if (
        is_teacher_available(teacher_a, day_a, time_a, availability)
        and is_teacher_available(teacher_b, day_b, time_b, availability)
        and (day_a, time_a) != (day_b, time_b)
    ):
        return True
    else:
        return False


# Create the CSP
class_schedule = CSP(class_info, domains, neighbors, constraint)

# Solve the CSP
solution = min_conflicts(class_schedule)

if(solution == None):
    print("Error , No Solution Founded")

else:
# Print the solution grouped by day
    schedule_by_day = {day: [] for day in days}

# Populate the schedule_by_day dictionary
    for class_, details in solution.items():
        day_time, room = details
        day, time = day_time
        schedule_by_day[day].append(f"Class: {class_[:-1]}, Time: {time}, Room: {room}")

# Print the schedule grouped by day
    for day, schedule in schedule_by_day.items():
        print(f"Day: {day}")
        if not schedule:
            print("  No classes scheduled.")
        else:
            for class_details in schedule:
                print(f"  {class_details}")
        print()