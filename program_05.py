WIDTH = 1280
HEIGHT = 640

# Class definition
class Game:
    def __init__(self, background_active, rooms_in_game):

        # we set the most important elements, some permanently
        self.background_active = background_active
        self.background_position = (0, 0)

        # elements related to our hero
        self.floor_level = 460
        self.hero = Actor("character-right-01.png")
        self.hero.pos = (WIDTH / 2, self.floor_level)

        # dictionary with room descriptions
        self.rooms = rooms_in_game

    def update_game(self):
        # this method will be called from the main program’s update() function

        pass

    def draw_scene(self):
        # this method will be called from the main program’s draw() function

        # we display the background
        screen.blit(self.background_active, self.background_position)
        # we display the hero based on his properties
        self.hero.draw()


class Key:
    def __init__(self, file_name, in_pocket, room_number, place_on_floor):
        """ self means *itself* - a specific key object instance """

        # these *self* object attributes are assigned from the parameters
        self.file_name = file_name
        self.in_pocket = in_pocket
        self.room_number = room_number
        self.place_on_floor = place_on_floor

    # for now, we do nothing
    pass


class Door:
    def __init__(self, room_number, door_position, next_room_number, open):
        """ self means *itself* - a specific door object instance """

        self.room_number = room_number
        # each door has fixed dimensions (236 pixels), so we calculate the left and right sides
        self.x_left_door = door_position - (236 / 2)
        self.x_right_door = door_position + (236 / 2)
        self.next_room_number = next_room_number
        self.open = open

    # for now, we do nothing
    pass


class Room:
    def __init__(self, room_number, room_name, can_move_lr, file_name, doors=[]):

        self.room_number = room_number
        self.room_name = room_name
        # if we can move from the room left or right we don't need
        # separate variables for directions left/right/up/down, we can use a 'flag'
        # with a different meaning depending on its value,
        # e.g. 0 – no direction, 1 - left only, 2 - right only, 3 - left and right
        self.can_move_lr = can_move_lr
        # filename containing the room’s background image
        self.file_name = file_name
        # list of doors in the room - by default empty list []
        self.doors = doors

    # for now, we do nothing
    pass


# main variables
background_active = "corridor-01.jpg"

# create keys, as *self* we assign variable names to key_
key_00 = Key("key-00.png", False, 11, 1025)
key_01 = Key("key-01.png", False, 17, 80)
key_02 = Key("key-02.png", False, 16, 850)
key_03 = Key("key-03.png", False, 4, 950)
key_04 = Key("key-04.png", False, 0, 370)

# we create doors according to the floor plan
# by default, each door will be open
door_00 = Door(0, 963, 5, True)
door_01 = Door(3, 962, 8, True)
door_02 = Door(5, 307, 15, True)
door_03 = Door(5, 967, 0, True)
door_04 = Door(6, 337, 11, True)
door_05 = Door(7, 932, 17, True)
door_06 = Door(8, 767, 3, True)
door_07 = Door(8, 327, 13, False)
door_08 = Door(11, 327, 6, True)
door_09 = Door(13, 327, 8, True)
door_10 = Door(15, 307, 5, True)
door_11 = Door(17, 932, 7, True)

# first, we create room descriptions according to our floorplan with new instances of the Room class
room_00 = Room(0, "Science 01", 2, "science-01.jpg", [door_00])
room_01 = Room(1, "Science 02", 1, " science-02.jpg")
room_03 = Room(3, "Gym 01", 2, "gym-01.jpg", [door_01])
room_04 = Room(4, "Gym 02", 1, "gym-02.jpg")
room_05 = Room(5, "Corridor 01 left", 2, "corridor-01.jpg", [door_02, door_03])
room_06 = Room(6, "Corridor 02", 3, "corridor-02.jpg", [door_04])
room_07 = Room(7, "Corridor 03", 3, "corridor-03.jpg", [door_05])
room_08 = Room(8, "Corridor 04 right", 1, "corridor-04.jpg", [door_06, door_07])
room_11 = Room(11, "WC", 0, "wc.jpg", [door_08])
room_13 = Room(13, "Auditorium", 0, "auditorium.jpg", [door_09]) #the Auditorium is not on the floorplan!
room_15 = Room(15, "Math 01", 2, "maths-01.jpg", [door_10])
room_16 = Room(16, "Math 02", 1, "maths-02.jpg")
room_17 = Room(17, "Computer science 01", 2, "computer-science-01.jpg", [door_11])
room_18 = Room(18, "Computer science 02", 1, "computer-science-02.jpg")


# next we create a dictionary corresponding to the numbering of rooms on the floorplan
rooms_in_game = {
    0: room_00,
    1: room_01,
    3: room_03,
    4: room_04,
    5: room_05,
    6: room_06,
    7: room_07,
    8: room_08,
    11: room_11,
    13: room_13,
    15: room_15,
    16: room_16,
    17: room_17,
    18: room_18,
}


# we create a game variable
game = Game(background_active, rooms_in_game)


def update():
    game.update_game()


def draw():
    game.draw_scene()
