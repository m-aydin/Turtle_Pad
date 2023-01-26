#Turtle Pad - Command Operated Turtle


#Imports
import time
import turtle
import sys

#Functions
def initialize_sprite():
    global GRID_VALUES
    global sprite
    global drawing_pad

    drawing_pad=turtle.getscreen()
    sprite=turtle.Turtle()

    drawing_pad.setup(GRID_VALUES[0]*GRID_VALUES[1],GRID_VALUES[0]*GRID_VALUES[1])

def get_commands(override=""):
    global COMMANDS

    if override != "":
        user_command=override.lower().split(" ")
    else:
        user_command=input("").lower().split(" ")

    if user_command[0] not in COMMANDS:
        print("Invalid Command\n")
        get_commands()
    elif user_command[0] not in COMMANDS[-3:] and len(user_command) == 1:
        print("Arguments Required, None Given\n")
        get_commands()
    
    if user_command[0] == COMMANDS[0]:                                   #move command
        move(user_command[1:])

    elif user_command[0] == COMMANDS[1]:                                 #circle command     
        try:
            user_command[1]=int(user_command[1])
        except:
            print("Integer Argument Required, Non-Integer Given\n")
            get_commands()

        if len(user_command[1:]) > 1:
            try:
                user_command[2]=int(user_command[2])
            except:
                print("Integer Argument Required, Non-Integer Given\n")  
                get_commands()

            if user_command[2] < -360 or user_command[2] > 360:
                print("Circle Sector Size Out Of Range")
                get_commands()
        else:
            user_command.append("360")

        circle(int(user_command[1]),int(user_command[2]))

    if user_command[0] == COMMANDS[3]:                                   #togglepen command
        toggle_pen()

    if user_command[0] == COMMANDS[4]:                                   #reset command
        reset()

    if user_command[0] == COMMANDS[2]:                                   #load command
        load(user_command[1])

    if user_command[0] == COMMANDS[5]:                                   #exit command
        exit()

def move(command_list):
    global MOVEMENT_BINDS
    global GRID_VALUES
    global sprite
    magnitude=1

    for current_command in command_list:
        if current_command == "":
            continue

        if current_command[0].isdigit():
            magnitude=int(current_command[0])
            current_command=current_command[1:]

        for current_move in [*current_command]:
            if current_move == MOVEMENT_BINDS[0][0]:      #forward/north
                sprite.setheading(MOVEMENT_BINDS[0][1])   
            elif current_move == MOVEMENT_BINDS[1][0]:    #backward/south
                sprite.setheading(MOVEMENT_BINDS[1][1])
            elif current_move == MOVEMENT_BINDS[2][0]:    #left/west
                sprite.setheading(MOVEMENT_BINDS[2][1])
            elif current_move == MOVEMENT_BINDS[3][0]:    #right/east
                sprite.setheading(MOVEMENT_BINDS[3][1])
            sprite.forward(GRID_VALUES[0]*magnitude)


def circle(diameter,sector_size):
    global GRID_VALUES
    global sprite
    
    sprite.circle(GRID_VALUES[0]*0.5*diameter,sector_size)

def toggle_pen():
    global sprite

    if sprite.isdown():
        sprite.up()
        sprite.fillcolor("red")
    else:
        sprite.down()
        sprite.fillcolor("black")


def reset():
    global sprite

    sprite.reset()
    print("\n")


def load(file_name):
    global sprite

    try:
        file_name_txt=open(file_name,"r")
    except:
        print("Invalid Text File Given\n")
        get_commands()
    
    sprite.speed(0)
    file_name=file_name_txt.readlines()

    for current_command in file_name:
        get_commands(current_command.strip("\n"))

    file_name_txt.close()
    sprite.speed(6)

def exit():
    global drawing_pad

    drawing_pad.bye()
    sys.exit()

#Constants
GRID_VALUES=[100,10]
MOVEMENT_BINDS=[["w",90],["s",270],["a",180],["d",0]]               #w is north, s is south, a is west, d is east
COMMANDS=["move","circle","load","togglepen","reset","exit"]

#Global Variables
sprite=""
drawing_pad=""

#Main Program
initialize_sprite()
while True:
    get_commands()