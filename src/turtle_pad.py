#Turtle Pad - Command Operated Turtle


#Imports
import traceback
import turtle
import sys

#Helper Functions
def initialize_turtle_pad():
    global SPRITE_COLOURS
    global sprite
    global drawing_pad

    drawing_pad=turtle.Screen()
    sprite=turtle.Turtle()

    drawing_pad.colormode(255)
    for current_colour in SPRITE_COLOURS:
        shape_override=turtle.Shape("compound")
        shape_override.addcomponent(sprite.get_shapepoly(),current_colour[1])
        drawing_pad.register_shape(current_colour[0],shape_override)

def debug_user_input_loop():
    global TEXT_COLOURS
    while True:
        try:
            eval(input(""))
        except Exception:
            print(TEXT_COLOURS[0]+"Warning, Error Encountered:\n"+TEXT_COLOURS[1]+traceback.format_exc()+"\n")

def save_recording():
    print("save_recording")

def load_recording(file_name):
    print("load_recording")

def command_parser(user_input=""):  #user_input: optional override of typical user input, used for drawing loading
    global COMMAND_BINDS
    global HEADING_BINDS
    global TEXT_COLOURS
    global is_recording
    multiplier=1

    if user_input == "":
        user_input=input("")
    user_input=user_input.strip("\n").split()

    if bind_list_comparison(COMMAND_BINDS,user_input[0],-1)[0] == 0:
        del user_input[0]
        if len(user_input) > 2:
            error("One Argument Required")
        elif len(user_input) == 2:
            if user_input[0].strip("-").isdigit() == False:
                error("Invalid Movement Multiplier")
            elif int(user_input[0]) < 0:
                error("Movement Multiplier Cannot Be Negative")
            else:
                multiplier=int(user_input[0])
                del user_input[0]

        if user_input[0].isalpha() == True:
            if bind_list_comparison(HEADING_BINDS,user_input[0],0)[0] == -1:
                error("Invalid Heading Bind")
            else:
                for current_move in [*user_input[0]]:
                    move(HEADING_BINDS[bind_list_comparison(HEADING_BINDS,current_move,0)[0]][1],multiplier)
        elif user_input[0].isdigit() == True:
            pass
        else:
            error("Invalid Heading")
    else:
        error("Command Not Found")

def set_sprite_colour(name):  #name: name of colour to set pen sprite to                                 
    global sprite
    sprite.shape(name)

def error(error_message):     #error_message: error message to display
    global TEXT_COLOURS
    global is_recording
    print(TEXT_COLOURS[0]+error_message+"\n\n"+TEXT_COLOURS[1])
    if is_recording:
        toggle_recording()
    else:
        command_parser()

def bind_list_comparison(input_binds,input_to_check,index_to_check):  #input_binds: 2D list where it is checked if all of input_to_check is in a certain column of the list /
    binds_list=[]                                                     #index_to_check: determines what column of 2D list input_binds checked / input_to_check: string of characters
    output_indexes=[]                                                 #where presence is detected in given column of 2D list input_binds

    if index_to_check == -1:
        for current_bind in input_binds:
            if input_to_check in current_bind:
                return([input_binds.index(current_bind)])
        else:
            return([-1])
    else:
        for current_bind in input_binds:
            binds_list.append(current_bind[index_to_check])

    for current_input_to_check in [*input_to_check]:
        try:
            output_indexes.append(binds_list.index(current_input_to_check))
        except:
            return([-1])
    else:
        return(output_indexes)
            

#Command Functions
def exit():
    global drawing_pad
    print(TEXT_COLOURS[0]+"Exiting...\n\n"+TEXT_COLOURS[1]) 
    drawing_pad.bye()
    sys.exit()

def reset():
    global TEXT_COLOURS   
    global sprite
    print(TEXT_COLOURS[0]+"Resetting...\n\n"+TEXT_COLOURS[1])          
    sprite.reset()

def toggle_pen():
    global SPRITE_COLOURS
    global sprite
    if sprite.isdown():
        sprite.up()
        set_sprite_colour(SPRITE_COLOURS[1][0])
    else:
        sprite.down()
        set_sprite_colour(SPRITE_COLOURS[0][0])

def toggle_recording():
    global SPRITE_COLOURS
    global TEXT_COLOURS
    global sprite
    global is_recording
    if not is_recording:
        is_recording=True
        print(TEXT_COLOURS[2]+"\n\nRecording Started"+TEXT_COLOURS[1])
        set_sprite_colour(SPRITE_COLOURS[2][0])
    else:
        is_recording=False
        print(TEXT_COLOURS[2]+"Recording Stopped\n\n"+TEXT_COLOURS[1])
        set_sprite_colour(SPRITE_COLOURS[0][0])
        save_recording()

def move(movement_heading,distance_multiplier):         #movement_heading: controls direction turtle moves in, eg 90 for north, 0 for east /       
    global BASE_GRID_SIZE                               #distance_multiplier: controls what default movement distance should be modified by,
    global sprite                                       #eg multiplier of 6 would make you go 6 as far, but multiplier of 0.5 would make you
    sprite.setheading(movement_heading)                 #go half as far
    sprite.forward(BASE_GRID_SIZE*distance_multiplier)    

def circle(size_multiplier,sector_size,draw_heading):   #size_multiplier: controls circle diameter / sector_size: controls how much of 
    global BASE_GRID_SIZE                               #circle drawn, eg sector size=180, you draw a semi-circle / draw_heading: 
    global HEADING_BINDS                                #controls what way circle is drawn, eg wd or north-east would make circle draw
    global sprite                                       #going up and to the right
                                                       
    if draw_heading[0] == HEADING_BINDS[0][0]:
        sprite.setheading(HEADING_BINDS[0][1])
        sign=1
    else:
        sprite.setheading(HEADING_BINDS[1][1])
        sign=-1

    if draw_heading[1] == HEADING_BINDS[3][0]:
        sign=sign*-1

    sprite.circle(BASE_GRID_SIZE*0.5*sign*size_multiplier,sector_size)   

#Constants
BASE_GRID_SIZE=100                                                                                     #controls base movement amount
HEADING_BINDS=[["w",90],["s",270],["a",180],["d",0]]                                                   #0: north / 1: south / 2: west / 3: east              
COMMAND_BINDS=[["move","m"],["circle","c"]]
SPRITE_COLOURS=[["base_colour",(0,0,0)],["disabled_colour",(255,0,0)],["recording_colour",(0,255,0)]]  #0: base colour / 1: disabled colour / 2: recording colour
TEXT_COLOURS=["\033[0;31m\033[1m","\033[0m","\033[0;32m\033[1m"]                                       #0: error colour / 1: normal colour / 2: recording colour

#Global Variables
sprite=""
drawing_pad=""
is_recording=False
recorded_commands=[]

#Main Program
initialize_turtle_pad()
#debug_user_input_loop()
while True: 
    command_parser()