from datetime import datetime

WIDTH = 1280
HEIGHT = 640

# Class definition
class Game:
    def __init__(self, background_active, rooms_in_game):

        # we set the most important elements, some permanently
        self.background_active = background_active
        self.background_position = (0, 0)
        self.game_start = False
        self.game_finish = False
        self.actual_room = 5
        self.start_time = None
        self.all_keys_found = False
        self.show_hidden_door = False
        self.enter_last_door = False
        self.shift_ok = True

        # graphics for starting and ending the game
        self.intro_canvas = Actor("intro-canvas.png")
        self.intro_canvas.pos = (640, -160)
        self.game_over_canvas = Actor("intro-gameover-canvas.png")
        self.game_over_canvas.pos = (320, -160)

        # elements related to our hero
        self.floor_level = 460
        self.hero = Actor("character-right-01.png")
        self.hero.pos = (WIDTH / 2, self.floor_level)
        # set the characters’s size
        self.hero.height = 256
        self.hero.width = 140
        self.hero.frame = 1
        self.animation_step = 15

        # dictionary with room descriptions
        self.rooms = rooms_in_game

        # keys
        self.pocket = Actor("pocket.png")
        self.pocket.pos = (1000, 100)
        self.keys_in_pocket = [key_00, key_01, key_02, key_03, key_04]

    def draw_intro(self):
        def draw_text(text, x_offset, y_offset, fontsize=20):
            screen.draw.text(
                text,
                (self.intro_canvas.x + x_offset, self.intro_canvas.y + y_offset),
                fontname="ptsansnarrowbold.ttf",
                fontsize=fontsize,
                color=(187, 96, 191),
            )

        # dispaly the game’s intro screen
        self.intro_canvas.draw()
        animate(self.intro_canvas, pos=(640, 320), duration=0.3, tween="linear")

        draw_text("Max goes back to school", -450, -200, fontsize=32)

        # introduction: game story, gameplay, and keys used in the game
        story = (
            "This adventure game takes Max, our main character "
            "through a journey of obstacles and puzzles to reach the grand finale "
            "The action takes place at seemingly the most boring "
            "place in the world - school! "
            "Maybe with Max, we can... stir things up a bit. "
            "Find and collect all the keys to unlock the auditorium "
            "for a concert with the pounding bass of Europe's hottest band! "
            "\n\n"
            "To quit the game - press the 'Q' key."
            "\n\n"
            "Press the SPACEBAR to start the game!"
        )

        screen.draw.text(
            story,
            (self.intro_canvas.x - 450, self.intro_canvas.y - 160),
            width=900,
            fontname="ptsansnarrowregular.ttf",
            fontsize=20,
            color=(0, 0, 0),
        )

        # description of the control keys
        draw_text("walk through the door", 200, -55)
        draw_text("go left", 120, 175)
        draw_text("pick-up key", 230, 175)
        draw_text("go right", 330, 175)

    def draw_pocket(self):
        self.pocket.draw()
        # setting the position / distance between keys
        key_pos = [-200, -100, 0, 100, 200]

        temp = 0
        # for each key in the list
        for key in self.keys_in_pocket:
            pos = (self.pocket.x + key_pos[temp] - 45, self.pocket.y - 10)
            temp += 1
            if key.in_pocket:
                # if we have a key -  display it from an image file at a specific position
                screen.blit(key.file_name, pos)
            else:
                # if we do not have a key, we display a question mark
                screen.blit("question-mark.png", pos)

    def hero_move(self, direction):

        # we get the flag indicating which way Max can move
        move_flag = self.rooms[self.actual_room].can_move_lr

        if direction == "right":
            # if possible, move the character
            if self.hero.x < WIDTH - self.hero.width:
                self.hero.x += self.animation_step
            else:
                if move_flag == 2 or move_flag == 3:
                    self.actual_room += 1
                    self.hero.x = 10

        if direction == "left":
            # if possible, move the character
            if self.hero.x > self.hero.width:
                self.hero.x -= self.animation_step
            else:
                if move_flag == 1 or move_flag == 3:
                    self.actual_room -= 1
                    self.hero.x = WIDTH - self.hero.width

        # we set the background for the new room
        new_background_image = self.rooms[self.actual_room].file_name
        self.background_active = new_background_image

        # set the appropriate image to animate the movement
        self.hero.image = f"character-{direction}-0{self.hero.frame}.png"
        # by increasing the image number, we next time load another
        # image, and therefore Max will appear to walk
        self.hero.frame += 1
        # there are 8 images, so if frame > 8
        if self.hero.frame > 8:
            # then we go back to 1
            self.hero.frame = 1

    def enter_door(self):
        # we get a dictionary element
        room = self.rooms[self.actual_room]
        if len(room.doors):
            for door in room.doors:
                if (
                    self.hero.x > door.x_left_door
                    and self.hero.x < door.x_right_door
                    and door.open
                    and self.shift_ok
                ):
                    self.shift_ok = False
                    # we get the number of the new room and the filename of its background
                    new_room = door.next_room_number
                    new_background_image = self.rooms[new_room].file_name
                    # we set the appropriate attributes
                    self.background_active = new_background_image
                    self.actual_room = new_room
                    # we unlock after half a second
                    clock.schedule_unique(self.shift_do, 0.5)
                    # break out of the for loop and end
                    break

    def shift_do(self):
        self.shift_ok = True

    def draw_key(self):
        # for each key in the game
        for key in self.keys_in_pocket:
            # if the key is not in your pocket and the current room
            # number is the same as the room number of the key
            if not key.in_pocket and self.actual_room == key.room_number:
                # we display the key
                screen.blit(key.file_name, (key.place_on_floor, 475))

    def get_key(self):
        def check_all_keys(keys):
            for any_key in keys:
                if any_key.in_pocket is False:
                    return False
            else:
                return True

        # for each key in the game
        for key in self.keys_in_pocket:
            # if the key is not in your pocket and the current room
            # number is the same as the room number of the key
            # and our character is close to the key
            if (
                not key.in_pocket
                and self.actual_room == key.room_number
                and (120 > self.hero.x - key.place_on_floor >= 0)
            ):
                # we set the key as found
                key.in_pocket = True
                # and check if we’ve found all the keys
                self.all_keys_found = check_all_keys(self.keys_in_pocket)

    def update_game(self):
        """ this method will be called from the main program’s update() function """

        if not self.game_start and keyboard.space:
            self.game_start = True
            self.start_time = datetime.now()

        if keyboard.q:
            quit()

        if self.game_start:
            if keyboard.right:
                self.hero_move("right")
            if keyboard.left:
                self.hero_move("left")
            if keyboard.up:
                self.enter_door()
            if keyboard.down:
                self.get_key()
            if self.all_keys_found:
                self.show_hidden_door = True

    def draw_scene(self):
        """ this method will be called from the main program’s draw() function """

        # we display the background
        screen.blit(self.background_active, self.background_position)

        if self.game_start:
            # we draw a key pocket
            self.draw_pocket()
            # draw a key if it’s in this room
            self.draw_key()
            # we display the hero based on his properties
            self.hero.draw()

        elif self.game_finish:
            pass
        else:
            self.draw_intro()


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
