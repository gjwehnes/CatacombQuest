from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
import GameObject


TREASURE_ROOM_LOCATION = 1
WINE_CELLAR_LOCATION = 2
DRAGONS_LAYER_LOCATION = 3
PASSAGE_WAY_A_LOCATION = 4
PASSAGE_WAY_B_LOCATION = 5
PASSAGE_WAY_C_LOCATION = 6
WEAPONS_STORAGE_LOCATION = 7
PASSAGE_WAY_D_LOCATION = 8
STARTING_POINT_LOCATION = 9
    
command_widget = None
image_label = None
description_widget = None
inventory_widget = None
north_button = None
south_button = None
east_button = None
west_button = None
root = None

refresh_location = True
refresh_objects_visible = True

current_location = STARTING_POINT_LOCATION
turns_in_room_with_dragon = 3

end_of_game = False
sword_found = False
dragon_killed = False
door_openend = False   

scroll_object = GameObject.GameObject("scroll", PASSAGE_WAY_B_LOCATION, True, True, False, "There are some barely readable words on it!")
sword_object = GameObject.GameObject("sword", WEAPONS_STORAGE_LOCATION, True, False, False, "Wow, it looks sharp!")
weapon_rack_object = GameObject.GameObject("weapon rack", WEAPONS_STORAGE_LOCATION, False, True, False, "Hey, there is a cool-looking sword")
key_object = GameObject.GameObject("key", DRAGONS_LAYER_LOCATION, True, False, False, "It is one of those old-fashioned keys that may open up a door!")
mouse_object = GameObject.GameObject( "mouse", PASSAGE_WAY_D_LOCATION, True, True, False, "The mouse insolently looks back at you.")
dragon_object = GameObject.GameObject("dragon", DRAGONS_LAYER_LOCATION, False, False, False, "That is one evil-looking dragon!")
door_object = GameObject.GameObject("door", PASSAGE_WAY_A_LOCATION, False, True, False, "The door is small, but extremely sturdy looking.  It has a key hole, and is locked")

game_objects = [scroll_object, sword_object, weapon_rack_object, key_object, mouse_object, dragon_object, door_object]

def perform_command(verb, noun):
    
    if (verb == "GO"):
        perform_go_command(noun)
    elif ((verb == "N") or (verb == "S") or (verb == "E") or (verb == "W")):
        perform_go_command(verb)        
    elif ((verb == "NORTH") or (verb == "SOUTH") or (verb == "EAST") or (verb == "WEST")):
        perform_go_command(noun)        
    elif (verb == "GET"):
        perform_get_command(noun)
    elif (verb == "PUT"):
        perform_put_command(noun)
    elif (verb == "LOOK"):
        perform_look_command(noun)        
    elif (verb == "KILL"):
        perform_kill_command(noun)        
    elif (verb == "READ"):
        perform_read_command(noun)        
    elif (verb == "OPEN"):
        perform_open_command(noun)
    else:
        print_to_description("huh?")       
        
def perform_go_command(direction):

    global current_location
    global refresh_location
    
    if (direction == "N" or direction == "NORTH"):
        new_location = get_location_to_north()
    elif (direction == "S" or direction == "SOUTH"):
        new_location = get_location_to_south()
    elif (direction == "E" or direction == "EAST"):
        new_location = get_location_to_east()
    elif (direction == "W" or direction == "WEST"):
        new_location = get_location_to_west()
    else:
        new_location = 0
        
    if (new_location == 0):
        print_to_description("You can't go that way!")
    else:
        current_location = new_location
        refresh_location = True

def perform_get_command(object_name):
    
    global refresh_objects_visible
    game_object = get_game_object(object_name)
    
    if not (game_object is None):
        if (game_object.location != current_location or game_object.visible == False):
            print_to_description("You don't see one of those here!")
        elif (game_object.movable == False):
            print_to_description("You can't pick it up!")
        elif (game_object.carried == True):
            print_to_description("You are already carrying it")
        else:
            #object can be picked up...
            #handle special conditions
            if (game_object == mouse_object):
                print_to_description("The mouse scurries away.")
            else:
                #pick up the object
                game_object.carried = True
                game_object.visible = False
                refresh_objects_visible = True
    else:
        print_to_description("You don't see one of those here!")

# 
def perform_put_command(object_name):

    global refresh_objects_visible
    game_object = get_game_object(object_name)
    
    if not (game_object is None):
        if (game_object.carried == False):
            print_to_description("You are not carrying one of those.")
        else:
            #put down the object
            game_object.location = current_location
            game_object.carried = False
            game_object.visible = True
            refresh_objects_visible = True
    else:
        print_to_description("You are not carrying one of those!")
# 
def perform_look_command(object_name):

    global sword_found
    global refresh_location
    global refresh_objects_visible
    
    game_object = get_game_object(object_name)
 
    if not (game_object is None):

        if ((game_object.carried == True) or (game_object.visible and game_object.location == current_location)):
            print_to_description(game_object.description)
        else:
            #recognized but not visible
            print_to_description("You can't see one of those!")
 
        #special cases - when certain objects are looked at, others are revealed!
        if ((game_object == weapon_rack_object) and (sword_found == False)):
            sowrd_found = True
            sword_object.visible = True
            weapon_rack_object.description = "It is empty"
            global refresh_objects_visible
            refresh_objects_visible = True

    else:
        if (object_name == ""):
            #generic LOOK
            refresh_location = True
            refresh_objects_visible = True
        else:
            #not visible recognized
            print_to_description("You can't see one of those!")

def perform_kill_command(object_name):

    global dragon_killed
    game_object = get_game_object(object_name)
 
    if not (game_object is None):
        if (game_object == mouse_object):
            print_to_description("Don't be cruel he hasn't done a thing to you!")
        elif (game_object == dragon_object):
            if (current_location != dragon_object.location):
                print_to_description("I don't see a dragon around here!")
            elif (dragon_killed):
                print_to_description("He's already quite dead.")
            elif (sword_object.carried == False):
                print_to_description("You put up a good fight, but ultimately you are not going kill a dragon")
                print_to_description("with your bare hands. Maybe you should look for a weapon of some sort?!")
                print_to_description("GAME OVER")
                global end_of_game
                end_of_game = True
            else:
                print_to_description("The dragon puts up quite the fight, but you emerge victorious, albeit a little burnt.")
                print_to_description("The dragon's corpse slowly disintegrates into a fine black powder, which drifts away in the draft.")
                print_to_description("Where the dragon was laying, you see something shiny!")
                key_object.visible = True
                dragon_killed = True
        else:
            print_to_description("You can't kill inanimate objects, silly!")
    else:
        #not visible recognized
        print_to_description("You can't kill what you can't see")

def perform_read_command(object_name):

    game_object = get_game_object(object_name)
 
    if not (game_object is None):
        if (game_object == scroll_object):
            if (scroll_object.carried):
                print_to_description("...days of old.... gold?...dragon...something something... bold")
            elif ((scroll_object.location == current_location) and (scroll_object.visible)):
                print_to_description("You can't read it from a distance.  You may want to pick it up (hint - use the GET command)")
            else:
                print_to_description("You can't find it!)")
        else:
            if ((game_object.visible == False) and (game_object.carried == False)):
                print_to_description("You can't read what you can't see, silly!")
            elif (game_object.location != current_location):
                print_to_description("You can't read what you can't see, silly!")
            else:
                print_to_description("There is no text on it")
    else:
        print_to_description("I am not sure which " + object_name + "you are refering to")
# 
def perform_open_command(object_name):

    global door_openend
    game_object = get_game_object(object_name)
 
    if not (game_object is None):
        if (game_object == door_object):
            if (key_object.carried):
                if (door_openend == True):
                    print_to_description("It is already opened!")
                else:
                    print_to_description("You unlock the door using your key.  The door slowly opens, creaking on it's hinges")
                    door_openend = True
                    door_object.description = "An open door"
            else: 
                print_to_description("It is locked, and you don't have the key!")
        else:
            print_to_description("You can't open one of those.")
    else:
        print_to_description("You don't see one of those here.")
                
def describe_current_location():
        
    if (current_location == TREASURE_ROOM_LOCATION):
        print_to_description("You are in a room filled with golden treasure!")
        print_to_description("You are rich beyond your wildest dreams")
        print_to_description("GAME OVER")
        global end_of_game
        end_of_game = True
    elif (current_location == WINE_CELLAR_LOCATION):
        print_to_description("You are in a musty wine cellar.  To your right (east), you see a dim red light")
    elif (current_location == DRAGONS_LAYER_LOCATION):
        print_to_description("You are in a small room with no other exit.")
        if (dragon_killed == False):
            print_to_description("In the middle of the room there is a fierce-looking dragon!")
    elif (current_location == PASSAGE_WAY_A_LOCATION):
        print_to_description("You are in a dark passageway sloping down towards the north") 
    elif (current_location == PASSAGE_WAY_B_LOCATION):
        print_to_description("You are in a dark passageway.")
    elif (current_location == PASSAGE_WAY_C_LOCATION):
        print_to_description("You are in a dark passageway.") 
    elif (current_location == WEAPONS_STORAGE_LOCATION):
        print_to_description("You are in a weapon storage room")
    elif (current_location == PASSAGE_WAY_D_LOCATION):
        print_to_description("You are in a dark passageway.")
    elif (current_location == STARTING_POINT_LOCATION):        
        print_to_description("You are in a cell, deep below the ground. A single shaft of light shines dimly from a barred window high above")        
    else:
        print_to_description("unknown location:" + current_location)

def set_current_image():
    
    if (current_location == TREASURE_ROOM_LOCATION):
        image_label.img = PhotoImage(file = 'res/hallway.gif') # change path to image as necessary
    elif (current_location == WINE_CELLAR_LOCATION):
        image_label.img = PhotoImage(file = 'res/hallway.gif') # change path to image as necessary
    elif (current_location == DRAGONS_LAYER_LOCATION):
        image_label.img = PhotoImage(file = 'res/altar_room.gif') # change path to image as necessary        
    elif (current_location == PASSAGE_WAY_A_LOCATION):
        #https://c1.staticflickr.com/6/5063/5789855128_a0c715ee50_b.jpg
        image_label.img = PhotoImage(file = 'res/dungeon-with-door.gif') # change path to image as necessary
    elif (current_location == PASSAGE_WAY_B_LOCATION):
        image_label.img = PhotoImage(file = 'res/hallway.gif') # change path to image as necessary
    elif (current_location == PASSAGE_WAY_C_LOCATION):
        image_label.img = PhotoImage(file = 'res/hallway.gif') # change path to image as necessary
    elif (current_location == WEAPONS_STORAGE_LOCATION):
        #http://i.imgur.com/SvdFV.jpg
        image_label.img = PhotoImage(file = 'res/weapons-rack.gif') # change path to image as necessary
    elif (current_location == PASSAGE_WAY_D_LOCATION):
        image_label.img = PhotoImage(file = 'res/hallway.gif') # change path to image as necessary
    elif (current_location == STARTING_POINT_LOCATION):
        image_label.img = PhotoImage(file = 'res/entrance.gif') # change path to image as necessary        
    else:
        image_label.img = PhotoImage(file = 'res/hallway.gif') # change path to image as necessary
        
    image_label.config(image = image_label.img)


def get_location_to_north():
    
    if (current_location == PASSAGE_WAY_A_LOCATION):
        return (TREASURE_ROOM_LOCATION if door_openend else 0)
    elif (current_location == PASSAGE_WAY_B_LOCATION):
        return WINE_CELLAR_LOCATION
    elif (current_location == WEAPONS_STORAGE_LOCATION):
        return PASSAGE_WAY_A_LOCATION
    elif (current_location == PASSAGE_WAY_D_LOCATION):
        return PASSAGE_WAY_B_LOCATION
    elif (current_location == STARTING_POINT_LOCATION):
        return PASSAGE_WAY_C_LOCATION
    else:
        return 0

def get_location_to_south():
    
    if (current_location == WINE_CELLAR_LOCATION):
        return PASSAGE_WAY_B_LOCATION
    elif (current_location == PASSAGE_WAY_A_LOCATION):
        return WEAPONS_STORAGE_LOCATION
    elif (current_location == PASSAGE_WAY_B_LOCATION):
        return PASSAGE_WAY_D_LOCATION
    elif (current_location == PASSAGE_WAY_C_LOCATION):
        return STARTING_POINT_LOCATION
    else:
        return 0

def get_location_to_east():
    
    if (current_location == WINE_CELLAR_LOCATION):
        return DRAGONS_LAYER_LOCATION
    elif (current_location == PASSAGE_WAY_B_LOCATION):
        return PASSAGE_WAY_C_LOCATION
    elif (current_location == WEAPONS_STORAGE_LOCATION):
        return PASSAGE_WAY_D_LOCATION
    else:
        return 0

def get_location_to_west():
    
    if (current_location == DRAGONS_LAYER_LOCATION):
        return WINE_CELLAR_LOCATION
    elif (current_location == PASSAGE_WAY_C_LOCATION):
        return PASSAGE_WAY_B_LOCATION
    elif (current_location == PASSAGE_WAY_D_LOCATION):
        return WEAPONS_STORAGE_LOCATION
    else:
        return 0
        
def get_game_object(object_name):
    sought_object = None
    for current_object in game_objects:
        if (current_object.name.upper() == object_name):
            sought_object = current_object
            break
    return sought_object

def describe_current_visible_objects():
    
    object_count = 0
    object_list = ""
    
    for current_object in game_objects:
        if ((current_object.location  == current_location) and (current_object.visible == True) and (current_object.carried == False)):
            object_list = object_list + ("," if object_count > 0 else "") + current_object.name
            object_count = object_count + 1
            
    print_to_description("You see: " + (object_list + "." if object_count > 0 else "nothing special.")) 

def describe_current_inventory():
    
    object_count = 0
    object_list = ""

    for current_object in game_objects:
        if (current_object.carried):
            object_list = object_list + ("," if object_count > 0 else "") + current_object.name
            object_count = object_count + 1
    
    inventory = "You are carrying: " + (object_list if object_count > 0 else "nothing")
    
    inventory_widget.config(state = "normal")
    inventory_widget.delete(1.0, END)
    inventory_widget.insert(1.0, inventory)
    inventory_widget.config(state = "disabled")

def handle_special_condition():
    
    global turns_in_room_with_dragon
    global end_of_game
    
    if ((current_location == DRAGONS_LAYER_LOCATION) and (dragon_killed == False) and (end_of_game == False)):
        turns_in_room_with_dragon -= 1
        if (turns_in_room_with_dragon == 2):
            print_to_description("The dragon's eyes slowly open, and he stares at you with obvious evil intent")
        elif (turns_in_room_with_dragon == 1):
            print_to_description("The dragon snorts, and a small blue flame appears at his nostrils.  He doesn't look very friendly!")
        elif (turns_in_room_with_dragon == 0):
            print_to_description("The dragon shoots a fireball at you and you are engulfed in flames")
            print_to_description("Your last thought is that the dragon must be guarding something...")
            print_to_description("GAME OVER")            
            end_of_game = True
         
def print_to_description(output, user_input=False):
    description_widget.config(state = 'normal')
    description_widget.insert(END, output)
    if (user_input):
        description_widget.tag_add("blue_text", CURRENT + " linestart", END + "-1c")
        description_widget.tag_configure("blue_text", foreground = 'blue')
    description_widget.insert(END, '\n')        
    description_widget.config(state = 'disabled')
    description_widget.see(END)

def build_interface():
    
    global command_widget
    global image_label
    global description_widget
    global inventory_widget
    global north_button
    global south_button
    global east_button
    global west_button    
    global root

    root = Tk()
    root.resizable(0,0)
    
    style = ttk.Style()
    style.configure("BW.TLabel", foreground="black", background="white")

    image_label = ttk.Label(root)    
    image_label.grid(row=0, column=0, columnspan =3,padx = 2, pady = 2)

    description_widget = Text(root, width =50, height = 10, relief = GROOVE, wrap = 'word')
    description_widget.insert(1.0, "Welcome to my game\n\nGood Luck!. ")
    description_widget.config(state = "disabled")
    description_widget.grid(row=1, column=0, columnspan =3, sticky=W, padx = 2, pady = 2)

    command_widget = ttk.Entry(root, width = 25, style="BW.TLabel")
    command_widget.bind('<Return>', return_key_enter)
    command_widget.grid(row=2, column=0, padx = 2, pady = 2)
    
    button_frame = ttk.Frame(root)
    button_frame.config(height = 150, width = 150, relief = GROOVE)
    button_frame.grid(row=3, column=0, columnspan =1, padx = 2, pady = 2)

    north_button = ttk.Button(button_frame, text = "N", width = 5)
    north_button.grid(row=0, column=1, padx = 2, pady = 2)
    north_button.config(command = north_button_click)
    
    south_button = ttk.Button(button_frame, text = "S", width = 5)
    south_button.grid(row=2, column=1, padx = 2, pady = 2)
    south_button.config(command = south_button_click)

    east_button = ttk.Button(button_frame, text = "E", width = 5)
    east_button.grid(row=1, column=2, padx = 2, pady = 2)
    east_button.config(command = east_button_click)

    west_button = ttk.Button(button_frame, text = "W", width = 5)
    west_button.grid(row=1, column=0, padx = 2, pady = 2)
    west_button.config(command = west_button_click)
    
    inventory_widget = Text(root, width = 30, height = 8, relief = GROOVE , state=DISABLED )
    inventory_widget.grid(row=2, column=2, rowspan = 2, padx = 2, pady = 2,sticky=W)
       
def set_current_state():

    global refresh_location
    global refresh_objects_visible

    if (refresh_location):
        describe_current_location()
        set_current_image()
    
    if (refresh_location or refresh_objects_visible):
        describe_current_visible_objects()

    handle_special_condition()
    set_directions_to_move()            

    if (end_of_game == False):
        describe_current_inventory()
    
    refresh_location = False
    refresh_objects_visible = False
    
    command_widget.config(state = ("disabled" if end_of_game else "normal"))

def north_button_click():
    print_to_description("N", True)
    perform_command("N", "")
    set_current_state()

def south_button_click():
    print_to_description("S", True)
    perform_command("S", "")
    set_current_state()

def east_button_click():
    print_to_description("E", True)
    perform_command("E", "")
    set_current_state()

def west_button_click():
    print_to_description("W", True)
    perform_command("W", "")
    set_current_state()

def return_key_enter(event):
    if( event.widget == command_widget):
        command_string = command_widget.get()
        print_to_description(command_string, True)

        command_widget.delete(0, END)
        words = command_string.split(' ', 1)
        verb = words[0]
        noun = (words[1] if (len(words) > 1) else "")
        perform_command(verb.upper(), noun.upper())
        
        set_current_state()

def set_directions_to_move():

    move_to_north = (get_location_to_north() > 0) and (end_of_game == False)
    move_to_south = (get_location_to_south() > 0) and (end_of_game == False)
    move_to_east = (get_location_to_east() > 0) and (end_of_game == False)
    move_to_west = (get_location_to_west() > 0) and (end_of_game == False)
    
    north_button.config(state = ("normal" if move_to_north else "disabled"))
    south_button.config(state = ("normal" if move_to_south else "disabled"))
    east_button.config(state = ("normal" if move_to_east else "disabled"))
    west_button.config(state = ("normal" if move_to_west else "disabled"))

def main():
    
    build_interface()
    set_current_state()
    #answer = simpledialog.askstring("Input", "What is your first name?", parent=root)    
    root.mainloop()
        
        
main()