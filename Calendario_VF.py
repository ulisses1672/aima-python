import sys
sys.path.append(r'D:\_MIAA\FIA\aima-python-master')

#from csp import *
# from notebook import psource, plot_NQueens

# %matplotlib inline
# Hide warnings in the matplotlib sections

import math
import warnings
warnings.filterwarnings("ignore")

from csp import CSP, min_conflicts
from collections import Counter

# Define the classes
classes = ["Math", "English", "History", "Science"]
quantity = [1, 2, 1,4]

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
    domains[class_] = [(time_slot, room) for time_slot in time_slots[:25] if time_slot in availability[teacher] for room in rooms]     #20 slots de tempo disponiveis para cada professor

# Define the neighbors
neighbors = {class_: [other_class for other_class in class_info if other_class != class_] for class_ in class_info}

# Define the constraints

def constraint(A, a, B, b):     # Check if the time slots are different and not consecutive
    if a[0] != b[0] and (a[0][0] != b[0][0] or abs(time_slots.index(a[0]) - time_slots.index(b[0])) > 1):
        # Check if the assignment attribute exists
        if hasattr(class_schedule, 'assignment'):
            # Count the number of lessons for each class in the morning and afternoon
            lessons_A_morning = sum(1 for value in class_schedule.assignment[A] if class_schedule.assignment[A] is not None and value[0][1] < 12)
            lessons_A_afternoon = sum(1 for value in class_schedule.assignment[A] if class_schedule.assignment[A] is not None and value[0][1] >= 12)
            lessons_B_morning = sum(1 for value in class_schedule.assignment[B] if class_schedule.assignment[B] is not None and value[0][1] < 12)
            lessons_B_afternoon = sum(1 for value in class_schedule.assignment[B] if class_schedule.assignment[B] is not None and value[0][1] >= 12)
            
            # Check if a class has more than 3 lessons in the morning or afternoon
            if lessons_A_morning > 3 or lessons_A_afternoon > 3 or lessons_B_morning > 3 or lessons_B_afternoon > 3:
                return False
            
            # Check if classes have most of the classes in the same room
            room_A = class_schedule.assignment[A][0][0] if class_schedule.assignment[A] is not None else None
            room_B = class_schedule.assignment[B][0][0] if class_schedule.assignment[B] is not None else None
            
            if room_A is not None and room_B is not None and room_A != room_B:
                return False
        
        return True
    
    return False

# Create the CSP
class_schedule = CSP(class_info, domains, neighbors, constraint)

# Solve the CSP
solution = min_conflicts(class_schedule)

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