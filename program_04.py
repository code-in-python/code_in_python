WIDTH = 1280
HEIGHT = 640

# Class definition
class Game:
    def __init__(self, background_active):

        # we set the most important elements, some permanently
        self.background_active = background_active
        self.background_position = (0, 0)

        # elements related to our hero
        self.floor_level = 460
        self.hero = Actor("character-right-01.png")
        self.hero.pos = (WIDTH / 2, self.floor_level)


    def update_game(self):
        """ this method will be called from the main program’s update() function """
        pass

    def draw_scene(self):
        """ this method will be called from the main program’s draw() function """
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


# main variables
background_active = "corridor-01.jpg"

# create keys, as *self* we assign variable names to key_
key_00 = Key("key-00.png", False, 11, 1025)
key_01 = Key("key-01.png", False, 17, 80)
key_02 = Key("key-02.png", False, 16, 850)
key_03 = Key("key-03.png", False, 4, 950)
key_04 = Key("key-04.png", False, 0, 370)


# we create a game variable
game = Game(background_active)

def update():
    game.update_game()

def draw():
    game.draw_scene()
