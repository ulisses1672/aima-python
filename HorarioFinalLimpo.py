import sys
sys.path.append(r'D:\_MIAA\FIA\aima-python-master')

# %matplotlib inline
# Hide warnings in the matplotlib sections

import math
import warnings
warnings.filterwarnings("ignore")
import random
from csp import *
from collections import Counter
from prettytable import PrettyTable



#Criar quantidade de aulas aleatorias para cada classe
def quantity_add(classe,quantity):
    # Generate a random total number of classes between 4 and 10
    desired_total_classes = random.randint(len(classe), 10)

    # Distribute the total randomly among the classes
    quantity = [1] * len(classe)  # Start with at least 1 for each class
    remaining_classes = desired_total_classes - len(classe)

# Distribute the remaining classes randomly
    for _ in range(remaining_classes):
        index = random.randint(0, len(classe) - 1)
        quantity[index] += 1

    return quantity

# VARIAVEIS
quantity = []

Lesi_classes = ['Math', 'English', 'History', 'Art', 'Music']
quantity = quantity_add(Lesi_classes,quantity)

Miaa_classes = ['Physics', 'Chemistry', 'Biology', 'Science', 'Physical_Education']
classes = Lesi_classes + Miaa_classes
quantity = quantity + quantity_add(Miaa_classes,quantity)

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
    "Teacher7": time_slots, # Teacher7 is available at any time
    "Teacher8": time_slots,
    "Teacher9": time_slots,
    "Teacher10": time_slots
    # Add availability for the rest of the teachers
}


# Dominio 
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

# Restrições
# Define the constraints
# Restrição de 2 aulas por dia
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
# Restrição nº de aulas por semana
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
# Restrição de aulas de Lesi e Miaa
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

# Restrição Aulas de Educação Fisica apenas na sala de Gym e Gym apenas com aulas de Educação Fisica
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

# Restrição de nº de alunos por sala
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
        and (class_a[:-1] == 'Lesi' or (room_a != 'Room2' or class_a[:-1] == 'Miaa')) # Restrição de nº de alunos por sala Lesi = 20 alunos e Miaa = 23 alunos
        and (class_b[:-1] == 'Lesi' or (room_b != 'Room2' or class_b[:-1] == 'Miaa'))):# Restrição de nº de alunos por sala Lesi = 20 alunos e Miaa = 23 alunos
        return True
    else:
        return False


# Create the CSP
class_schedule = CSP(class_info, domains, neighbors, constraint)

# Solve the CSP
solution = min_conflicts(class_schedule)


# Impressão da solução
# Create a table with columns for each day, room, and teacher
combined_table = PrettyTable()
combined_table.field_names = ["Class", "Category", "Time", "Room", "Teacher", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Initialize a variable to track the last category
last_category = None

# Populate the combined table
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

    # Add a line between Lesi and Miaa classes
    if last_category is not None and last_category != category:
        combined_table.add_row(["----", "----", "----", "----", "----", "----", "----", "----", "----", "----"])

    # Add rows to the combined table
    combined_table.add_row([
        class_name,
        category,
        time,
        room,
        teacher,
        "X" if day == "Monday" else "",
        "X" if day == "Tuesday" else "",
        "X" if day == "Wednesday" else "",
        "X" if day == "Thursday" else "",
        "X" if day == "Friday" else ""
    ])

    last_category = category

# Print the combined table
print(combined_table)