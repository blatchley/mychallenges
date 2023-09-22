import pygame

from .textbox import Textbox
from .itembox import Itembox
from .sprites import *
from .config import *
import sys, os


class Game:
    def __init__(self, connection : PsygameChannel):
        self.channel = connection
        pygame.init()
        self.screen = pygame.display.set_mode((1024,768))
        self.clock = pygame.time.Clock()
        self.running = True
        self.user_inputs = []
        self.current_input = None
        self.current_level = 1
        self.movecount = 0
        self.player_alive = True
        self.items_picked_up = {}
        self.active_item = ""
        self.items_collected = []
        self.gates_open = []
        self.level_change = 0

        # Data received from server each move
        self.movedata = {}

        self.psyduck_sprites = {}

        # Load in graphics
        imagespath = os.path.dirname(__file__) 
        self.font = pygame.font.Font(imagespath + '/arial.ttf', 32)
        self.psyduck_sprites["left"] = Spritesheet(imagespath + "/img/psyduck.png")
        self.psyduck_sprites["up"] = Spritesheet(imagespath + "/img/psyduck.png")
        self.psyduck_sprites["down"] = Spritesheet(imagespath + "/img/psyduck.png")
        self.psyduck_sprites["right"] = Spritesheet(imagespath + "/img/psyduck_flipped.png")
        self.psyduck_sprites["left_sg"] = Spritesheet(imagespath + "/img/psyduck_sg.png")
        self.psyduck_sprites["up_sg"] = Spritesheet(imagespath + "/img/psyduck_sg.png")
        self.psyduck_sprites["down_sg"] = Spritesheet(imagespath + "/img/psyduck_sg.png")
        self.psyduck_sprites["right_sg"] = Spritesheet(imagespath + "/img/psyduck_flipped_sg.png")
        self.confusion_overlay = Spritesheet(imagespath + "/img/confusion.png")
        self.terrain_spritesheet = Spritesheet(imagespath + "/img/terrain.png")
        self.item_spritesheet = Spritesheet(imagespath + "/img/items.png")
        self.tree_spritesheet = Spritesheet(imagespath + "/img/48x48 trees.png")

        self.textbox = Textbox((0, self.screen.get_height() - (self.screen.get_height() // 5), self.screen.get_width(), self.screen.get_height()), "", self.font, False)
        self.itembox = Itembox(self, (self.screen.get_width()-64, 0, self.screen.get_width(), 64), True, self.font)
        
        
        pygame.key.set_repeat(500, 150)


    # Renders tilemap!
    def create_tilemap(self, tilemap, level):
        for i, row in enumerate(tilemap):
            if isinstance(row, str):
                for j, column in enumerate(row):
                    Ground(self,j, i, level)
                    if column == "B":
                        Block(self,j,i)
                    if column == "W":
                        Wall(self,j,i)
                    if column == "G":
                        if not (j,i) in self.gates_open:
                            Gate(self,j,i)
                    if column == "T":
                        Tree(self,j,i)
                    if column == "P":
                        p = Player(self,j,i)
                    if column == "L":
                        Lava(self,j,i)
                    if column == "A":
                        Water(self,j,i)
                    if column == "R":
                        Road(self,j,i)
                    if column == "F":   # text is on server
                        Flag(self,j,i)
                    if column == "S":
                        Sign(self, j, i, "") #text is on server
                    if column == "X":
                        DangerousGround(self,j,i)
                    if column == "Y":
                        DangerousGround2(self,j,i)
                    if column == "1":
                        TownExit(self,j,i,1)
                    if column == "2":
                        TownExit(self,j,i,2)
                    if column == "3":
                        TownExit(self,j,i,3)
                    if column == "4":
                        TownExit(self,j,i,4)
                    if column == "5":
                        TownExit(self,j,i,5)
            elif isinstance(row, tuple):
                if row[0] == "item":
                    print(f"Check if {(self.current_level, row[1][0], row[1][1])} in items_collected")
                    if (self.current_level, row[1][0], row[1][1]) not in self.items_collected:
                        Item(self, row[1][0], row[1][1], row[2])
        
        p.recenter_screen()

    def load_level(self,levelid):
        self.player_alive = True
        self.is_confused = False

        self.all_sprites.empty()
        self.blocks.empty()
        self.dangerous.empty()
        self.lava.empty()
        self.water.empty()
        self.teleporters.empty()
        self.signs.empty()
        self.flags.empty()
        self.gates.empty()
        self.items.empty()

        if levelid == 1:
            self.current_level = 1
            self.create_tilemap(level_1, levelid)
        elif levelid == 2:
            self.current_level = 2
            self.create_tilemap(level_2, levelid)
        elif levelid == 3:
            self.current_level = 3
            self.create_tilemap(level_3, levelid)
        elif levelid == 4:
            self.current_level = 4
            self.create_tilemap(level_4, levelid)
        elif levelid == 5:
            self.current_level = 5
            self.create_tilemap(level_5, levelid)
        

    def new(self):
        # start game
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.flags = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.gates = pygame.sprite.LayeredUpdates()
        self.lava = pygame.sprite.LayeredUpdates()
        self.water = pygame.sprite.LayeredUpdates()
        self.dangerous = pygame.sprite.LayeredUpdates()
        self.teleporters = pygame.sprite.LayeredUpdates()
        self.signs = pygame.sprite.LayeredUpdates()
        self.items = pygame.sprite.LayeredUpdates()

        
        # Load first level
        self.load_level(1)

    
    def main(self):
        self.update()
        self.draw()
        #game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()

        self.running = False

    def handle_event(self, event):
        # Handle quit
        if event.type == pygame.QUIT:
            self.playing = False
            self.running = False
            pygame.quit()
            sys.exit()
            return 

        # Handle user input
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                self.playing = False
                self.running = False
                pygame.quit()
                sys.exit()

            if event.key in VALID_BUTTONS:
                self.user_inputs.append(event.key)
                return
            return

    def events(self):
        # Reset user input
        self.current_input = None

        # game loop events
        for event in pygame.event.get():
            self.handle_event(event)
        
        # If no user input in queue, wait until there is
        while not self.user_inputs:
            event = pygame.event.wait()
            self.handle_event(event)

        # set movement using first element of movement list. 
        if self.user_inputs:
            self.current_input, self.user_inputs = self.user_inputs[0], self.user_inputs[1:]
        returned = self.channel.client_send(str(self.current_input)) 

        self.movedata = returned


    def update(self):
        # game loop updates
        self.all_sprites.update()

        if self.level_change:
            nextlevel = self.level_change
            self.level_change = 0
            self.load_level(nextlevel)

        if not self.player_alive:
            # Reset items
            self.items_picked_up.pop(self.active_item, None)
            self.active_item = ""
            self.items_collected = []
            self.gates_open = []
            self.load_level(self.current_level)
        

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        if self.textbox.active and self.textbox.text != "":
            self.textbox.draw(self.screen)
        
        if self.itembox.active:
            self.itembox.active_item = self.active_item
            if self.active_item != "":
                self.itembox.active_amount = self.items_picked_up[self.active_item]
            self.itembox.draw(self.screen)
            
        pygame.display.update()

    def game_over(self):
        pass





def launch_game(connection):
    g = Game(connection)
    g.new()
    while g.running:
        g.main()
        g.game_over()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    launch_game()