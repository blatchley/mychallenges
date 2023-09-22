import pygame
from .config import *
import math
import random

class Spritesheet:
    def __init__(self,file):
        self.sheet = pygame.image.load(file).convert_alpha()

    def get_sprite(self,x,y,width,height, offset = (0,0)):
        sprite = pygame.Surface([width,height], pygame.SRCALPHA)
        sprite.blit(self.sheet, offset, (x,y,width,height))
        return sprite


class Item(pygame.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.items
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.orig_x = x
        self.orig_y = y

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.type = type

        if self.type == "key":
            self.image = self.game.terrain_spritesheet.get_sprite(64,960,self.width,self.height)
        elif self.type == "cool_sunglasses":
            self.image = self.game.terrain_spritesheet.get_sprite(96,960,self.width,self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Player(pygame.sprite.Sprite):
    def __init__(self,game, x, y):
        
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)



        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.image = self.game.psyduck_sprites["left"].get_sprite(0,0,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def recenter_screen(self):
        # recenter screen on player by moving ALL sprites
        # Calculate offset of psyduck from center
        x_offset = (self.rect.x // TILESIZE) - (WIN_WIDTH // TILESIZE // 2)
        y_offset = (self.rect.y // TILESIZE) - (WIN_HEIGHT // TILESIZE // 2)
        # shift all sprites (including psyduck) to recenter
        for sprite in self.game.all_sprites:
            sprite.rect.x -= x_offset * TILESIZE
            sprite.rect.y -= y_offset * TILESIZE

    def update(self):
        self.movement()

        # update played position
        self.rect.x +=  self.x_change * TILESIZE
        self.rect.y +=  self.y_change * TILESIZE

        
        self.recenter_screen()

        self.x_change = 0
        self.y_change = 0
        self.check_lava_collision()
        self.check_teleporter_collision()
        self.check_dangerous_collision()
        self.check_water_collision()
        if not self.check_item_collision():
            pass
        if not self.check_sign_collision():
            self.game.textbox.active = False

    # update Player state by applying movement
    def handle_movement(self):
        keys = self.game.current_input
        
        if keys == pygame.K_a:
            keys = pygame.K_LEFT
        if keys == pygame.K_s:
            keys = pygame.K_DOWN
        if keys == pygame.K_d:
            keys = pygame.K_RIGHT
        if keys == pygame.K_w:
            keys = pygame.K_UP

        # handle if psyduck is confused
        if "confused" in self.game.movedata:
            self.game.is_confused = True
            if not "confusion_rotation" in self.game.movedata:
                print("ERROR: confused but no confusion rotation.")
            else:
                # Don't rotate if standing still
                if not keys == pygame.K_h:
                    confusion_rotation = self.game.movedata["confusion_rotation"]
                    movelist = [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN]
                    keys = movelist[(movelist.index(keys) + confusion_rotation) % 4]
        else:
            self.game.is_confused = False


        if keys == None:
            return
        if keys == pygame.K_LEFT:
            self.x_change -= 1
            self.facing = 'left'
        if keys == pygame.K_RIGHT:
            self.x_change += 1
            self.facing = 'right'
        if keys == pygame.K_UP:
            self.y_change -= 1
            self.facing = 'up'
        if keys == pygame.K_DOWN:
            self.y_change += 1
            self.facing = 'down'

        if self.game.active_item == "cool_sunglasses":
            self.image = self.game.psyduck_sprites[self.facing + "_sg"].get_sprite(0,0,self.width,self.height)
        else:
            self.image = self.game.psyduck_sprites[self.facing].get_sprite(0,0,self.width,self.height)

        if self.game.is_confused:
            print("confused")
            confusion_overlay = self.game.confusion_overlay.get_sprite(0,0, self.width, self.height)
            self.image.blit(confusion_overlay, (0,0))
        
    # test if move would cause collision
    def check_block_collision(self):
        self.rect.x += self.x_change * TILESIZE
        self.rect.y += self.y_change * TILESIZE
        collision =  pygame.sprite.spritecollide(self, self.game.blocks, False)
        
        for b in collision:
            print(b)
            print(b.rect.x)
            print(b.rect.y)

        self.rect.x -= self.x_change * TILESIZE
        self.rect.y -= self.y_change * TILESIZE
        return collision
    
    # test if currently colliding with lava :psyduck:
    def check_lava_collision(self):
        collision =  pygame.sprite.spritecollide(self, self.game.lava, False)
        if collision:
            self.game.player_alive = False
            print("You stood on lava and died")
        
    def check_dangerous_collision(self):
        collision =  pygame.sprite.spritecollide(self, self.game.dangerous, False)
        if collision:
            self.game.player_alive = False
            print("You died")
        
    def check_water_collision(self):
        collision =  pygame.sprite.spritecollide(self, self.game.water, False)
        if collision:
            self.game.player_alive = False
            print("You... Drowned? Psyduck pls!?")
   
    # test if currently colliding with a teleporter/town exit
    def check_teleporter_collision(self):
        collision =  pygame.sprite.spritecollide(self, self.game.teleporters, False)
        if collision:
            print(collision[0].target_level)
            self.game.level_change = collision[0].target_level
            print(f"level_change = {self.game.level_change}")

    def check_sign_collision(self):
        if "sign" in self.game.movedata:
            if "sign_text" not in self.game.movedata:
                print("ERROR: sign_text missing while sign was set.")
                return False
            self.game.textbox.active = True
            self.game.textbox.text = self.game.movedata["sign_text"]
            print(self.game.movedata["sign_text"])
            return True

        collision =  pygame.sprite.spritecollide(self, self.game.signs, False)
        if collision:
            print("Warning: server doesn't think your on a sign. Possible Desync?")
            self.game.textbox.active = True
            self.game.textbox.text = "Warning: server doesn't think your on a sign. Possible Desync?"
            return True
        return False

    def check_item_collision(self):
        collision =  pygame.sprite.spritecollide(self, self.game.items, False)

        if "item_pickup" in self.game.movedata:
            if "item_type" not in self.game.movedata:
                print("ERROR: item_type missing while item_pickup is set.")
                return False
            item_type = self.game.movedata["item_type"]

            if item_type in self.game.items_picked_up:
                self.game.items_picked_up[item_type] += 1
            else:
                self.game.items_picked_up[item_type] = 1
            self.game.active_item = item_type
            self.game.items_collected.append((self.game.current_level, collision[0].orig_x, collision[0].orig_y))

            collision[0].kill()
            return True

        if collision:
            print("Warning: server doesn't think your on a item. Possible Desync?")
            self.game.textbox.active = True
            self.game.textbox.text = "Warning: server doesn't think your on a item. Possible Desync?"
            return True
        return False
    
    def check_gate_collision(self):
        self.rect.x += self.x_change * TILESIZE
        self.rect.y += self.y_change * TILESIZE
        collision =  pygame.sprite.spritecollide(self, self.game.gates, False)
        
        for b in collision:
            print(b)
            print(b.rect.x)
            print(b.rect.y)

        self.rect.x -= self.x_change * TILESIZE
        self.rect.y -= self.y_change * TILESIZE

        if collision and "key" in self.game.items_picked_up:
            if self.game.items_picked_up["key"] > 0:
                collision[0].kill()
                self.game.items_picked_up["key"] -= 1
                self.game.gates_open.append((collision[0].orig_x, collision[0].orig_y))

                if self.game.items_picked_up["key"] <= 0:
                    self.game.active_item = ""
                return False
        return collision

    def movement(self):
        # set x_change and y_change from user input
        self.handle_movement()

        # premove check for legality
        if self.check_block_collision() or self.check_gate_collision():
            print("collided with something, move ignored")
            self.x_change = 0
            self.y_change = 0
        else:
            if "blocked" in self.game.movedata:
                print("Warning: Server thought you were blocked here but client didn't.")
                print("@@ POTENTIAL DESYNC? @@")




####
# Rendering code
# collision blocks (impassable terrain)
# death lava (ground texture that kills on contact)
# death water (ground texture that kills on contact)
# death dangerousground (ground texture that kills on contact)
# town exits (teleport to other levels)
# ground (varies graphically per level)
####

class Block(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(960,448,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Wall(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64,996,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Gate(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = GATE_LAYER
        self.groups = self.game.all_sprites, self.game.gates
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.orig_x = x
        self.orig_y = y

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(96,996,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Water(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.water
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        offsets = [i*32 for i in range(3)]
        self.image = self.game.terrain_spritesheet.get_sprite(32*27 + random.choice(offsets), 5*32,self.width,self.height)
            
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Tree(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        offsets = [i*48 for i in range(4)]
        self.image = self.game.tree_spritesheet.get_sprite(random.choice(offsets),0,48,48)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Flag(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.flags
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(0,960,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class TownExit(pygame.sprite.Sprite):
    def __init__(self,game,x,y,target_level):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.teleporters
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        offsets = [i*32 for i in range(3)]
        self.image = self.game.terrain_spritesheet.get_sprite(928 + (x%2)*32, 640 + random.choice(offsets),self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.target_level = target_level



class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y, level):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        if level == 1 or level == 4:
            # get varied textures
            offsets = [i*32 for i in range(3)]
            self.image = self.game.terrain_spritesheet.get_sprite(0 + random.choice(offsets),352,self.width,self.height)
        elif level == 2:
            self.image = self.game.terrain_spritesheet.get_sprite(384+64,160,self.width,self.height)
        elif level == 3:
            offsets = [i*32 for i in range(3)]
            self.image = self.game.terrain_spritesheet.get_sprite(384 + random.choice(offsets),160,self.width,self.height)
        else:
            self.image = self.game.terrain_spritesheet.get_sprite(384+64,160,self.width,self.height)
            
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class DangerousGround(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.dangerous
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = self.game.terrain_spritesheet.get_sprite(288,160,self.width,self.height)
            
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class DangerousGround2(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = self.game.terrain_spritesheet.get_sprite(288,160,self.width,self.height)
            
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Road(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = LAVA_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        # get varied textures
        offsets = [i*32 for i in range(3)]
        self.image = self.game.terrain_spritesheet.get_sprite(928 + (x%2)*32, 640 + random.choice(offsets),self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Lava(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = LAVA_LAYER
        self.groups = self.game.all_sprites, self.game.lava
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        # variance in lava
        offsets = [0,32,64]
        self.image = self.game.terrain_spritesheet.get_sprite(480 + random.choice(offsets),160,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Sign(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text):
        self.game = game
        self._layer = SIGN_LAYER
        self.groups = self.game.all_sprites, self.game.signs
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.text = text

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = self.game.terrain_spritesheet.get_sprite(32,960,self.width,self.height)
            
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
