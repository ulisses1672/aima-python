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
from csp import *
from collections import Counter

# Define the classes
Lesi_classes = ['Math', 'English', 'History', 'Art', 'Music']
Miaa_classes = ['Physics', 'Chemistry', 'Biology', 'Science', 'Physical_Education']
classes = Lesi_classes + Miaa_classes

# Generate random class quantities
min_quantity = 1
max_total_classes = 10
quantity = []

# Generate a random total number of classes between 4 and 10
desired_total_classes = random.randint(len(classes), 10)

# Distribute the total randomly among the classes
quantity = [1] * len(classes)  # Start with at least 1 for each class
remaining_classes = desired_total_classes - len(classes)

# Distribute the remaining classes randomly
for _ in range(remaining_classes):
    index = random.randint(0, len(classes) - 1)
    quantity[index] += 1

class_info = [f"{class_name}{i+1}" for class_name, count in zip(classes, quantity) for i in range(count)]

# Define the rooms
rooms = ["Room1", "Room2", "Room3", "Gym"]

# Define the days
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Define the time slots for each day
time_slots = [(day, time) for day in days for time in ["9AM", "11AM", "1PM", "3PM"]]

# Define the teachers for each class
teachers = {
    "Math": "Teacher1", "English": "Teacher2", "History": "Teacher3", "Science": "Teacher4",
    "Art": "Teacher5", "Music": "Teacher6", "Physics": "Teacher7", "Chemistry": "Teacher8",
    "Biology": "Teacher9", "Physical_Education": "Teacher10"
}

# Define the availability of each teacher
availability = {
    "Teacher1": [("Monday", "9AM"),("Monday", "11AM"), ("Tuesday", "1PM"), ("Tuesday", "3PM")],
    "Teacher2": [("Monday", "9AM"),("Monday", "11AM"), ("Monday", "1PM"), ("Monday", "3PM"),("Tuesday", "1PM"), ("Tuesday", "3PM")],
    "Teacher3": [("Monday", "9AM"),("Monday", "11AM"), ("Monday", "1PM"), ("Monday", "3PM"),("Friday", "9AM"),("Friday", "11AM"), ("Friday", "1PM"), ("Friday", "3PM")],
    "Teacher4":  [("Monday", "9AM"),("Monday", "11AM"), ("Tuesday", "9AM"), ("Tuesday", "11AM") , ("Tuesday", "1PM"), ("Tuesday", "3PM"),("Wednesday", "9AM"),("Wednesday", "11AM"), ("Wednesday", "1PM"), ("Wednesday", "3PM"),("Thursday", "9AM"),("Thursday", "11AM"), ("Thursday", "1PM"), ("Thursday", "3PM"),("Friday", "11AM"), ("Friday", "1PM"), ("Friday", "3PM")],
    "Teacher5": [("Wednesday", "1PM"), ("Wednesday", "3PM"), ("Thursday", "1PM"), ("Thursday", "3PM")],
    "Teacher6": [("Tuesday", "9AM"), ("Tuesday", "11AM"), ("Wednesday", "9AM"), ("Wednesday", "11AM")],
    "Teacher7": time_slots,
    "Teacher8": time_slots,
    "Teacher9": time_slots,
    "Teacher10": time_slots
    # Add availability for the rest of the teachers
}



# Define the domains
index = 0
domains = {}
domainTotal = {}

for class_ in class_info:
    className = class_[:-1]
    teacher = teachers[className]
    index = index + 1
    domains[class_] = [(time_slot, room) for time_slot in time_slots[:25] if time_slot in availability[teacher] for room in rooms]  # 25 slots de tempo disponiveis para cada professor

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

def check_classes_on_day(schedule, specified_day):
    day_class_count = {}

    for class_name, ((day, time), room) in schedule.items():
        if day == specified_day:
            if class_name[:-1] in day_class_count:
                day_class_count[class_name[:-1]] += 1
                # Check if the count exceeds 2
                if day_class_count[class_name[:-1]] > 2:
                    return True
            else:
                day_class_count[class_name[:-1]] = 1

    return False

def check_days_per_week(schedule, class_name):
    days_count = Counter()
    counte = 0
    
    for other_class, ((day, _), _) in schedule.items():
        if other_class[:-1] == class_name[:-1]:
            days_count[day] += 1

    if(len(days_count)<=4):
        return False
    else:
        return True

def constraint(class_a, time_room_a, class_b, time_room_b):
    day_a, time_a = time_room_a[0]
    room_a = time_room_a[1]

    day_b, time_b = time_room_b[0]
    room_b = time_room_b[1]


    if check_days_per_week(class_schedule.current, class_a):
        return False
    if check_days_per_week(class_schedule.current, class_b):
        return False
    
    if (check_classes_on_day(class_schedule.current, day_a)):
        return False
    if (check_classes_on_day(class_schedule.current, day_b)):
        return False
    
    
    teacher_a = get_teacher_by_class(class_a[:-1], teachers)
    teacher_b = get_teacher_by_class(class_b[:-1], teachers)

    # Check if both time slots and rooms are available, if teachers are available,
    # and if the room capacity is sufficient
    if (is_teacher_available(teacher_a, day_a, time_a, availability)
        and is_teacher_available(teacher_b, day_b, time_b, availability)
        and (day_a, time_a) != (day_b, time_b)):
        return True
    else:
        return False

"""" 
#Aulas de Educação Fisica apenas na sala de Gym
def constraint(class_a, time_room_a, class_b, time_room_b):
    day_a, time_a = time_room_a[0]
    room_a = time_room_a[1]

    day_b, time_b = time_room_b[0]
    room_b = time_room_b[1]

    if check_days_per_week(class_schedule.current, class_a):
        return False
    if check_days_per_week(class_schedule.current, class_b):
        return False
    
    if (check_classes_on_day(class_schedule.current, day_a)):
        return False
    if (check_classes_on_day(class_schedule.current, day_b)):
        return False
    
    teacher_a = get_teacher_by_class(class_a[:-1], teachers)
    teacher_b = get_teacher_by_class(class_b[:-1], teachers)

    # Check if both time slots and rooms are available, if teachers are available,
    # and if the room capacity is sufficient
    if (
        is_teacher_available(teacher_a, day_a, time_a, availability)
        and is_teacher_available(teacher_b, day_b, time_b, availability)
        and (day_a, time_a) != (day_b, time_b)
    ):
        # New constraint: Physical_Education can only be taught in the room "Gym"
        if class_a[:-1] == "Physical_Education" and room_a != "Gym":
            return False
        if class_b[:-1] == "Physical_Education" and room_b != "Gym":
            return False
        
        return True
    else:
        return False
"""""

#Aulas de Educação Fisica apenas na sala de Gym e Gym apenas com aulas de Educação Fisica
def constraint(class_a, time_room_a, class_b, time_room_b):
    day_a, time_a = time_room_a[0]
    room_a = time_room_a[1]

    day_b, time_b = time_room_b[0]
    room_b = time_room_b[1]

    if check_days_per_week(class_schedule.current, class_a):
        return False
    if check_days_per_week(class_schedule.current, class_b):
        return False
    
    if (check_classes_on_day(class_schedule.current, day_a)):
        return False
    if (check_classes_on_day(class_schedule.current, day_b)):
        return False
    
    teacher_a = get_teacher_by_class(class_a[:-1], teachers)
    teacher_b = get_teacher_by_class(class_b[:-1], teachers)

    # Check if both time slots and rooms are available, if teachers are available,
    # and if the room capacity is sufficient
    if (is_teacher_available(teacher_a, day_a, time_a, availability)
        and is_teacher_available(teacher_b, day_b, time_b, availability)
        and (day_a, time_a) != (day_b, time_b)
        and ((class_a[:-1] == 'Physical_Education' and room_a == 'Gym') or (class_a[:-1] != 'Physical_Education' and room_a != 'Gym'))
        and ((class_b[:-1] == 'Physical_Education' and room_b == 'Gym') or (class_b[:-1] != 'Physical_Education' and room_b != 'Gym'))):
        return True
    else:
        return False

#Restrição de nº de alunos por sala
def student_count_constraint(class_a, time_room_a, class_b, time_room_b):
    day_a, time_a = time_room_a[0]
    room_a = time_room_a[1]

    day_b, time_b = time_room_b[0]
    room_b = time_room_b[1]

    if check_days_per_week(class_schedule.current, class_a):
        return False
    if check_days_per_week(class_schedule.current, class_b):
        return False
    
    if (check_classes_on_day(class_schedule.current, day_a)):
        return False
    if (check_classes_on_day(class_schedule.current, day_b)):
        return False
    
    teacher_a = get_teacher_by_class(class_a[:-1], teachers)
    teacher_b = get_teacher_by_class(class_b[:-1], teachers)

    # Check if both time slots and rooms are available, if teachers are available,
    # and if the room capacity is sufficient
    if (is_teacher_available(teacher_a, day_a, time_a, availability)
        and is_teacher_available(teacher_b, day_b, time_b, availability)
        and (day_a, time_a) != (day_b, time_b)
        and (class_a[:-1] == 'Lesi' or (room_a != 'Room2' or class_a[:-1] == 'Miaa'))
        and (class_b[:-1] == 'Lesi' or (room_b != 'Room2' or class_b[:-1] == 'Miaa'))):
        return True
    else:
        return False


# Create the CSP
class_schedule = CSP(class_info, domains, neighbors, constraint)

# Solve the CSP
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
    class_name = class_[:-1]
    teacher = teachers[class_name]

    # Determine if the class belongs to Lesi or Miaa
    if class_name in Lesi_classes:
        category = "Lesi"
    elif class_name in Miaa_classes:
        category = "Miaa"
    else:
        category = "Unknown"

    schedule_by_day[day].append(f"Lesson: {class_name}, Turma: {category}, Time: {time}, Room: {room}")

# Print the schedule grouped by day
for day, schedule in schedule_by_day.items():
    print(f"Day: {day}")
    if not schedule:
        print("  No classes scheduled.")
    else:
        for class_details in schedule:
            print(f"  {class_details}")
    print()
