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

from constraint import Problem, AllDifferentConstraint, FunctionConstraint

# Define the classes, rooms, days, teachers, availability, and time slots
classes = ["Math", "English", "History", "Science"]
quantity = [1, 2, 1, 2]

class_info = [f"{class_name}{i+1}" for class_name, count in zip(classes, quantity) for i in range(count)]

rooms = ["Room1", "Room2", "Room3", "Room4", "Room5", "Room6", "Room7", "Room8"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
teachers = {"Math": "Teacher1", "English": "Teacher2", "History": "Teacher3", "Science": "Teacher4"}
availability = {
    "Teacher1": [("Monday", "9AM"), ("Tuesday", "11AM"), ("Wednesday", "1PM"), ("Thursday", "3PM"), ("Friday", "5PM")],
    "Teacher2": [("Monday", "9AM"), ("Tuesday", "11AM"), ("Wednesday", "1PM"), ("Thursday", "3PM"), ("Friday", "5PM")],
    "Teacher3": [("Monday", "9AM"), ("Tuesday", "11AM"), ("Wednesday", "1PM"), ("Thursday", "3PM"), ("Friday", "5PM")],
    "Teacher4": [("Monday", "9AM"), ("Tuesday", "11AM")]
}
time_slots = [(day, time) for day in days for time in ["9AM", "11AM", "1PM", "3PM", "5PM"]]

# Define the domains
index = 0
domains = {}

for class_ in class_info:
    className = class_[:-1]
    teacher = teachers[className]
    index = index + 1
    domains[class_] = [(time_slot, room) for time_slot in time_slots[:25] if time_slot in availability[teacher] for room in rooms]

# Create the CSP problem
class_schedule = Problem()

# Add variables and domains
for class_, class_domain in domains.items():
    class_schedule.addVariable(class_, class_domain)

# Add function constraint to ensure that classes on the same day have different times
def different_times(*times):
    return len(set(times)) == len(times)

for day in days:
    classes_on_day = [class_ for class_ in class_info if class_.startswith(day[0])]
    class_schedule.addConstraint(FunctionConstraint(different_times), classes_on_day)

# Solve the problem
solution = class_schedule.getSolution()

# Print the solution grouped by day
schedule_by_day = {day: [] for day in days}

# Populate the schedule_by_day dictionary
for class_, details in solution.items():
    day_time, room = details
    day, time = day_time
    schedule_by_day[day].append(f"Class: {class_}, Time: {time}, Room: {room}")

# Print the schedule grouped by day
for day, schedule in schedule_by_day.items():
    print(f"Day: {day}")
    if not schedule:
        print("  No classes scheduled.")
    else:
        for class_details in schedule:
            print(f"  {class_details}")
    print()
