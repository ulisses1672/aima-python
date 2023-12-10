
# %matplotlib inline
# Hide warnings in the matplotlib sections

import sys
import math
import warnings
warnings.filterwarnings("ignore")
import random
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from csp import *
from collections import Counter
from prettytable import PrettyTable


#Funcao para criar quantidade de aulas aleatorias para cada classe
def quantity_add(classe,quantity):
    #Gera um número total aleatório de classes entre 4 e 10
    desired_total_classes = random.randint(len(classe), 10)

    #Distribui o total aleatoriamente entre as classes
    quantity = [1] * len(classe)  #Começa com pelo menos 1 de quantidade para cada classe
    remaining_classes = desired_total_classes - len(classe)

    #Distribua as classes restantes aleatoriamente
    for _ in range(remaining_classes):
        index = random.randint(0, len(classe) - 1)
        quantity[index] += 1

    return quantity

#VARIAVEIS
quantity = []

#Classe Lesi
Lesi_classes = ['Math', 'English', 'History', 'Art', 'Music']
quantity = quantity_add(Lesi_classes,quantity)

#Classe Miaa
Miaa_classes = ['Physics', 'Chemistry', 'Biology', 'Science', 'Physical_Education']
classes = Lesi_classes + Miaa_classes
quantity = quantity + quantity_add(Miaa_classes,quantity)

#Informação de todas as classes total (de Lesi e de Miaa)
class_info = [f"{class_name}{i+1}" for class_name, count in zip(classes, quantity) for i in range(count)]

#Defina as salas
rooms = ["Room1", "Room2", "Room3", "Gym"]

#Defina os dias
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Defina os time slots de cada dia
time_slots = [(day, time) for day in days for time in ["9AM", "11AM", "1PM", "3PM"]]

#Defina os professores de cada turma
teachers = {
    "Math": "Teacher1", "English": "Teacher2", "History": "Teacher3", "Science": "Teacher4",
    "Art": "Teacher5", "Music": "Teacher6", "Physics": "Teacher7", "Chemistry": "Teacher8",
    "Biology": "Teacher9", "Physical_Education": "Teacher10"
}

#Defina a disponibilidade de Horas e Dias de cada professor
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
}


#Dominio 
index = 0
domains = {}
domainTotal = {}

for class_ in class_info:
    className = class_[:-1]
    teacher = teachers[className]
    index = index + 1
    domains[class_] = [(time_slot, room) for time_slot in time_slots[:25] if time_slot in availability[teacher] for room in rooms]  # 25 slots de tempo disponiveis para cada professor

#Defina os neighbors
neighbors = {class_: [other_class for other_class in class_info if other_class != class_] for class_ in class_info}

#Funcao para ver se um professor esta disponivel no tempo e dia
def is_teacher_available(teacher, day, time, availability):
    if teacher in availability:
        for available_day, available_time in availability[teacher]:
            if available_day == day and available_time == time:
                return True
    return False

#Funcao para receber um professor com a classe
def get_teacher_by_class(class_name, teachers):
    return teachers.get(class_name, None)

#Funcao dar check a quantidade
def checkQuantity(quantity):
    for value in quantity:
        if value > 2:
            return True  
    return False

#Restrições
#Define the constraints

#Restrição de 2 aulas por dia
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

#Restrição nº de aulas por semana (Disciplinas podem ter so ate 4 dias diferentes da semana)
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
    

#Constraint/Restriçôes para Lesi e Miaa usando as funcoes anteriores 
#Nota: Aulas de Educação Fisica apenas é sempre só na sala de Gym
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

    #Verifica se os horários e as salas estão disponíveis, se os professores estão disponíveis,
    # e se a capacidade da sala é suficiente
    if (is_teacher_available(teacher_a, day_a, time_a, availability)
        and is_teacher_available(teacher_b, day_b, time_b, availability)
        and (day_a, time_a) != (day_b, time_b)
        and ((class_a[:-1] == 'Physical_Education' and room_a == 'Gym') or (class_a[:-1] != 'Physical_Education' and room_a != 'Gym'))
        and ((class_b[:-1] == 'Physical_Education' and room_b == 'Gym') or (class_b[:-1] != 'Physical_Education' and room_b != 'Gym'))):
        return True
    else:
        return False


#Cria o CSP
class_schedule = CSP(class_info, domains, neighbors, constraint)

#Resolve o CSP
solution = min_conflicts(class_schedule)


# Impressão da solução
# Cria uma tabela com colunas para cada dia, sala e professor
combined_table = PrettyTable()
combined_table.field_names = ["Class", "Category", "Time", "Room", "Teacher", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Defina a ordem crescente dos horários
time_order = ["9AM", "11AM", "1PM", "3PM"]

# Função para adicionar uma linha à tabela combinada
def add_row_to_table(class_, details, category):
    day_time, room = details
    day, time = day_time
    class_name = class_[:-1]
    teacher = teachers[class_name]

    # Adiciona uma linha à tabela combinada
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

# Preenche a tabela combinada para Lesi classes
combined_table.add_row(["----", "----", "----", "----", "----", "----", "----", "----", "----", "----"])
for time_slot in time_order:
    for class_, details in solution.items():
        if class_[:-1] in Lesi_classes:
            if details[0][1] == time_slot:
                add_row_to_table(class_, details, "Lesi")

# Preenche a tabela combinada para Miaa classes
combined_table.add_row(["----", "----", "----", "----", "----", "----", "----", "----", "----", "----"])
for time_slot in time_order:
    for class_, details in solution.items():
        if class_[:-1] in Miaa_classes:
            if details[0][1] == time_slot:
                add_row_to_table(class_, details, "Miaa")

# Imprima a tabela combinada
print(combined_table)
