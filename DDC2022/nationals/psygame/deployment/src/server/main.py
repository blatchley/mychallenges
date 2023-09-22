import pygame

from .sprites import *
from .config import *
import sys, os


# Server game class
class Game:
    def __init__(self):
        pygame.init()
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        self.screen = pygame.display.set_mode((1024,768))
        self.clock = pygame.time.Clock()
        self.running = True
        self.movedata = {}
        self.current_input = None
        self.current_level = 1
        self.movecount = 0
        self.player_alive = True
        self.items_picked_up = {}
        self.active_item = ""
        self.items_collected = []
        self.gates_open = []


        self.level_change = 0
        self.is_confused = False
       
        pygame.key.set_repeat(500, 150)


    def create_tilemap(self, tilemap, level):
        for i, row in enumerate(tilemap):
            if isinstance(row, str):
                for j, column in enumerate(row):
                    Ground(self,j, i, level)
                    if column == "B":
                        Block(self,j,i)
                    if column == "T":
                        Tree(self,j,i)
                    if column == "W":
                        Wall(self,j,i)
                    if column == "G":
                        if not (j,i) in self.gates_open:
                            Gate(self,j,i)
                    if column == "P":
                        p = Player(self,j,i)
                    if column == "L":
                        Lava(self,j,i)
                    if column == "A":
                        Water(self,j,i)
                    if column == "R":
                        Road(self,j,i)
                    if column == "F":
                        Flag(self,j,i)
                    if column == "C":
                        Confusion(self,j,i)
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
                if row[0] == "sign":
                    Sign(self, row[1][0], row[1][1], row[2])
                elif row[0] == "item":
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
        self.items.empty()
        self.gates.empty()

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
        self.lava = pygame.sprite.LayeredUpdates()
        self.water = pygame.sprite.LayeredUpdates()
        self.dangerous = pygame.sprite.LayeredUpdates()
        self.teleporters = pygame.sprite.LayeredUpdates()
        self.signs = pygame.sprite.LayeredUpdates()
        self.confusion = pygame.sprite.LayeredUpdates()
        self.items = pygame.sprite.LayeredUpdates()
        self.gates = pygame.sprite.LayeredUpdates()

        
        # Load first level
        self.load_level(1)
        
    def main(self):
        self.update()
        self.draw()
        #game loop

    def receive_input(self, move):
        if move == "exit":
            self.running = False
            pygame.quit()
            sys.exit()
        
        elif self.playing:
            if self.events(move):
                self.update()
                self.draw()
                return self.movedata
            else:
                self.movedata["failure"] = f"invalid input: {move} was not in allowed keys to press"
                print("sever error: invalid input")
                return self.movedata
        else:
            self.running = False
            pygame.quit()
            sys.exit()

    def events(self, move):
        # Reset user input
        self.movedata = {}
        self.current_input = move
        if move in VALID_BUTTONS:
            self.movedata["move"] = move
            self.movedata["step"] = self.movecount
            self.movecount += 1
            return True
        else:
            return False



    def update(self):
        # game loop updates
        self.all_sprites.update()

        if self.level_change:
            nextlevel = self.level_change
            self.level_change = 0
            self.load_level(nextlevel)

        if not self.player_alive:
            self.movedata["dead"] = True

            # Reset items
            self.items_picked_up.pop(self.active_item, None)
            self.active_item = ""
            self.items_collected = []
            self.gates_open = []
            self.load_level(self.current_level)
        

    def draw(self):
        self.all_sprites.draw(self.screen)

    def game_over(self):
        pass


def launch_game():
    g = Game()
    g.new()
    g.main()
    # game logic ticks over when "receive_input" is called
    return g
    
if __name__ == "__main__":
    launch_game()