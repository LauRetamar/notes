import sqlite3
import colorama
import os

#
def ClearConsole():
    os.system('cls' if os.name=='nt' else 'clear')

#set colors
colorama.init(autoreset=True) 

#db
connection = sqlite3.connect('notes.db')
cursor = connection.cursor()

def CreateLists():
    response = cursor.execute(f'SELECT count(name) FROM sqlite_master WHERE type="table" AND name="tasks"')
    if response.fetchone()[0] == 0:
        cursor.execute(f'CREATE TABLE tasks(task, done, listid);')
        connection.commit()
    response = cursor.execute(f'SELECT count(name) FROM sqlite_master WHERE type="table" AND name="lists"')
    if response.fetchone()[0] == 0:
        cursor.execute(f'CREATE TABLE lists(name);')
        connection.commit()
    return

def NewTask(listid, task):
    cursor.execute(f'INSERT INTO tasks VALUES("{task}", 0, {listid})')
    connection.commit()
    return

def MarkTaskAsDone(rowid):
    cursor.execute(f'UPDATE tasks SET done = 1 WHERE rowid == {rowid}')
    connection.commit()
    return

def RemoveTask(rowid):
    cursor.execute(f'DELETE FROM tasks WHERE rowid == {rowid}')
    connection.commit()
    return

def NewList(listName):
    cursor.execute(f'INSERT INTO lists VALUES("{listName}")')
    connection.commit()
    return

def GetTaskFromList(listid):
    result = cursor.execute(f'SELECT rowid, task, done FROM tasks WHERE listid == {listid}')
    return result

def GetLists():
    result = cursor.execute(f'SELECT rowid, name FROM lists')
    return result


#functions
def ChooseOption(option, param, listid):
    if option == 'a':
        NewTask(listid, param)
        return
    elif option == 'c':
        NewList(param)
        return
    elif option == 'r':
        RemoveTask(param)
        return
    elif option == 'd':
        MarkTaskAsDone(param)
        return
    else:
        return

#create tables
CreateLists()

#interface
option = ''
listid = 0

while(option != 's'):
    ClearConsole()

    #lists
    print('#######  LISTS  #######')
    data = GetLists()
    for a in data:
        if str(a[0]) == listid:
            print(colorama.Fore.LIGHTMAGENTA_EX + '# ' + str(a[0])  + '.  ' + str(a[1]))
        else:
            print('# ' + str(a[0]) + '.  '+ str(a[1]))

    #tasks
    print('#######  TASKS  #######')
    print('#')
    data = GetTaskFromList(listid)
    for a in data:
        if (a[2] == 1):
            print(colorama.Fore.LIGHTGREEN_EX + '# ' + str(a[0]) + '.  ' + a[1])
        else:
            print('# ' + str(a[0]) + '.  ' + a[1])

    print('#')
    print('#')
    print('#')
    print('# a: nueva tarea')
    print('# d: marcar tarea como finalizada')
    print('# r: eliminar tarea')
    print('# c: crear lista')
    print('# v: cambiar de lista')
    print('# s: salir')

    choice = input()
    option = choice[0:1]
    param = choice[2:]

    #list control
    if option == 'v':
        listid = param

    ChooseOption(option, param, listid)



#bye
cursor.close()
connection.close()


