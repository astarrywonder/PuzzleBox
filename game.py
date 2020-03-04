"""
doorsound.wav
    # Credit to Michael Baradari
    # Release under CC-BY 3.0
jump.wav
    # Credit to Jesús Lastra
    # Public Domain CC0
box_drop.wav
    # Credit to  Dan Knoflicek
    # Release under CC-BY 3.0
Sprites
    # Source: opengameart.org
    # Name from source: Sara and Star
    # Artist: Mandi Paugh
"""
import os
import sys
import time
from pathlib import Path
import pygame as pg
import yaml

config = {
     'window_width': 1280
    ,'window_height': 720
    ,'screen_width': 1280
    ,'screen_height': 720
    ,'framerate': 60.0
    ,'window_caption': 'Puzzle Game'
    ,'color_backgroud': (0, 0, 0, 1)
    ,'intro_backImg': 'background.jpg'
    ,'game_characterpath': "characters/"
    ,'game_spritepath': "sprites/"
    ,'game_tilesize': 24
    ,'gameover_backImg': "GameOver.jpg"
}

class Game_intro:
    def __init__(self):
        self.sf_window = pg.display.get_surface()
        self.sf_screen = pg.Surface((config['screen_width'], config['screen_height']))
        self.done = False
        self.clock = pg.time.Clock()
        self.framerate = config['framerate']
        self.keys = pg.key.get_pressed()

        self.backImg = pg.image.load(config['intro_backImg'])
        self.button_start = self.Button("Start", 600, 450, 100, 50, (0, 200, 0), (0, 255, 0))
        self.button_continue = self.Button("Continue", 600, 550, 100, 50, (0, 0, 100), (0, 0, 255))
        self.button_quit = self.Button("Quit", 600, 650, 100, 50, (200, 0, 0), (255, 0, 0))

        self.result = ""

    class Button:
        def __init__(self, msg, x, y, width, height, ic, ac):
            self.rect = pg.Rect(x, y, width, height)
            self.color_inactive = ic
            self.color_active = ac

            self.mouse_pos = (0, 0)
            self.mouse_click = False
            self.hover = False

            self.color = self.color_inactive
            self.msg = msg
            self.font = pg.font.SysFont("comicsansms", 20)
            self.textcolor = (0, 0, 0)

        def get_event(self, event):
            self.mouse_pos = pg.mouse.get_pos()
            self.mouse_click = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == pg.BUTTON_LEFT:
                    self.mouse_click = True

        def update(self):
            if self.rect.collidepoint(self.mouse_pos):
                self.color = self.color_active
                if self.mouse_click == True:
                    return True
            else:
                self.color = self.color_inactive
                return False

        def draw(self, surface):
            pg.draw.rect(surface, self.color, self.rect)
            textobj = self.font.render(self.msg, 1, self.textcolor)
            textrect = textobj.get_rect()
            textrect.center = self.rect.center
            surface.blit(textobj, textrect)

    def event_loop(self):
        for event in pg.event.get():
            self.keys = pg.key.get_pressed()
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                pg.quit()
                sys.exit()
            self.button_start.get_event(event)
            self.button_continue.get_event(event)
            self.button_quit.get_event(event)

    def update(self):
        if self.button_start.update():
            self.result = "start"
            self.done = True
        if self.button_continue.update():
            self.result = "continue"
            self.done = True
        if self.button_quit.update():
            self.result = "quit"
            self.done = True

    def draw(self):
        self.sf_screen.fill((56, 142, 142))
        self.sf_screen.blit(self.backImg, (0, 0))
        self.button_start.draw(self.sf_screen)
        self.button_continue.draw(self.sf_screen)
        self.button_quit.draw(self.sf_screen)

        self.sf_window.blit(pg.transform.scale(self.sf_screen, self.sf_window.get_size()), (0, 0))

    def display_fps(self):
        caption = "{} - FPS: {:.2f}".format(config['window_caption'], self.clock.get_fps())
        pg.display.set_caption(caption)

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.update()
            self.draw()
            pg.display.update()
            self.clock.tick(self.framerate)
            self.display_fps()
        return self.result

class Game_over:
    def __init__(self):
        self.sf_window = pg.display.get_surface()
        self.sf_screen = pg.Surface((config['screen_width'], config['screen_height']))
        self.done = False
        self.clock = pg.time.Clock()
        self.framerate = config['framerate']
        self.keys = pg.key.get_pressed()

        self.backImg = pg.image.load(config['gameover_backImg'])

    def event_loop(self):
        for event in pg.event.get():
            self.keys = pg.key.get_pressed()
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE] or self.keys[pg.K_q]:
                self.done = True

    def draw(self):
        self.sf_screen.fill((56, 142, 142))
        self.sf_screen.blit(self.backImg, (0, 0))

        self.sf_window.blit(pg.transform.scale(self.sf_screen, self.sf_window.get_size()), (0, 0))

    def display_fps(self):
        caption = "{} - FPS: {:.2f}".format(config['window_caption'], self.clock.get_fps())
        pg.display.set_caption(caption)

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.draw()
            pg.display.update()
            self.clock.tick(self.framerate)
            self.display_fps()

class Player:
    def __init__(self):
        self.img_jill = pg.image.load(config['game_characterpath'] + "Jill/Right.gif").convert()
        self.img_jack = pg.image.load(config['game_characterpath'] + "Jack/Right.gif").convert()
        self.img = self.img_jill
        self.img_changed = False
        self.rect_sprite = self.img.get_rect()
        self.rect_range1 = pg.Rect(0, 0, config['game_tilesize']/2, config['game_tilesize']-4)
        self.rect_range2 = pg.Rect(0, 0, config['game_tilesize']/2, config['game_tilesize']-4)
        self.rect = self.rect_sprite
        self.facing_left = False

        self.current_collision_type = {'top': False, 'bottom': False, 'right': False, 'left': False}

        self.moving_left = False
        self.moving_right = False
        self.moving_speed = 4

        self.moving_jumping = False
        self.jump_speed = -6
        self.vertical_momentum = 0
        self.air_timer = 0

        self.interact_pressed = False

        self.jump_sound = pg.mixer.Sound('./sounds/jump.wav')
        self.jump_sound.set_volume(0.3)


        self.busy_box = 0
        self.carrying = False
        self.bag = None

        # self.telported = False

    def teleport(self, location):
        self.rect.x = location[0]
        self.rect.y = location[1]

    def switch_char(self):
        if self.img == self.img_jill:
            self.img = self.img_jack
        elif self.img == self.img_jack:
            self.img = self.img_jill

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key in [pg.K_c]:
                if not self.img_changed:
                    self.switch_char()
                    self.img_changed = True
            if event.key in [pg.K_k]:
                if not self.interact_pressed:
                    self.interact_pressed = True
        self.get_event_always(event)


    def get_event_always(self, event):
        if event.type == pg.KEYDOWN:
            if event.key in [pg.K_LEFT, pg.K_a]:
                self.moving_left = True
            if event.key in [pg.K_RIGHT, pg.K_d]:
                self.moving_right = True
            if event.key in [pg.K_UP, pg.K_j, pg.K_w]:
                self.moving_jumping = True

        if event.type == pg.KEYUP:
            if event.key in [pg.K_LEFT, pg.K_a]:
                self.moving_left = False
            if event.key in [pg.K_RIGHT, pg.K_d]:
                self.moving_right = False
            if event.key in [pg.K_UP, pg.K_j, pg.K_w]:
                self.moving_jumping = False

        if event.type == pg.KEYUP:
            if event.key in [pg.K_c]:
                self.img_changed = False
            if event.key in [pg.K_k]:
                self.interact_pressed = False

    def update(self, impassable, logicobjs, movebox):
        tiles = impassable.copy()
        if self.facing_left:
            self.rect_range1.right = self.rect.left
            self.rect_range2.right = self.rect.left
        else:
            self.rect_range1.left = self.rect.right
            self.rect_range2.left = self.rect.right
        self.rect_range1.top = self.rect.top
        self.rect_range2.top = self.rect_range1.bottom + 1
        movement = [0, 0]

        if self.busy_box == 0:
            if self.moving_left:
                movement[0] -= self.moving_speed
            if self.moving_right:
                movement[0] += self.moving_speed

        if movement[0] > 0:
            self.facing_left = False
        if movement[0] < 0:
            self.facing_left = True

        if self.moving_jumping and self.air_timer < 6 and self.current_collision_type['bottom']:
            self.jump_sound.play()
            self.vertical_momentum = self.jump_speed
        elif not self.moving_jumping and self.air_timer > 6 and self.vertical_momentum < 0:
            self.vertical_momentum = 0

        if self.current_collision_type['top'] and self.vertical_momentum < 0:
            self.vertical_momentum = 0

        movement[1] += self.vertical_momentum
        self.vertical_momentum += 0.3

        for logic in logicobjs:
            if logicobjs[logic].type in ['ClosedBarrier']:
                if not logicobjs[logic].activated:
                    tiles[logic] = logicobjs[logic]
                else:
                    tiles.pop(logic, None)

        for box in movebox:
            if not movebox[box].carried:
                tiles[box] = movebox[box]
            else:
                tiles.pop(box, None)

        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.rect, self.current_collision_type = self.move(collision_types, self.rect, movement, tiles, self.bag)

        if self.current_collision_type['bottom']:
            self.air_timer = 0
            self.vertical_momentum = 0
        else:
            self.air_timer += 1

        if self.busy_box > 0:
            self.busy_box -= 1


    def collision_test(self, rect, tiles): # Public Domain by DaFluffyPotato
        hit_list = []
        for key in tiles:
            if rect.colliderect(tiles[key].rect):
                hit_list.append(tiles[key].rect)
        return hit_list

    def move(self, collision_types, rect, movement, tiles, bag): # Public Domain by DaFluffyPotato
        rect.x += movement[0]
        temprect = rect.copy()
        if not bag == None:
            bag.rect.x += movement[0]
            temprect.union_ip(bag.rect)
        hit_list = self.collision_test(temprect, tiles)
        for tile in hit_list:
            if movement[0] > 0:
                if not bag == None:
                    bag.rect.right = tile.left
                    rect.right = tile.left
                else:
                    rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                if not bag == None:
                    bag.rect.left = tile.right
                    rect.left = tile.right
                else:
                    rect.left = tile.right
                collision_types['left'] = True
        rect.y += movement[1]
        temprect = rect.copy()
        if not bag == None:
            bag.rect.y += movement[1]
            temprect.union_ip(bag.rect)
        hit_list = self.collision_test(temprect, tiles)
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                if not bag == None:
                    bag.rect.top = tile.bottom
                    rect.top = bag.rect.bottom
                else:
                    rect.top = tile.bottom
                collision_types['top'] = True

        if not bag == None:
            if rect.colliderect(bag.rect):
                bag.rect.bottom = rect.top

        return rect, collision_types

    def draw(self,screen):
        screen.blit(pg.transform.flip(self.img, self.facing_left, False), (self.rect.x, self.rect.y))

class Tile:
    def __init__(self, unscaled_x, unscaled_y, type):
        self.type = type
        self.img = pg.image.load(config['game_spritepath'] + self.type + '.png').convert()
        self.rect = self.img.get_rect()
        self.rect.x = unscaled_x * config['game_tilesize']
        self.rect.y = unscaled_y * config['game_tilesize']

    def draw(self, screen):
        screen.blit(self.img, (self.rect.x, self.rect.y))

class Helpbox(Tile):
    def __init__(self, unscaled_x, unscaled_y, text):
        super(Helpbox, self).__init__(unscaled_x, unscaled_y, 'helpbox')
        self.activated = False

        self.text = text
        self.font = pg.font.SysFont('freesansbold.ttf', 32)
        self.textcolor = (255, 0, 0)
        self.textlocation = (round(config['screen_width'] / 2), config['screen_height'] - 24)

    def update(self, player):
        if self.rect.colliderect(player.rect):
            self.activated = True
        else:
            self.activated = False

    def draw(self, screen):
        screen.blit(self.img, (self.rect.x, self.rect.y))
        # screen.blit(pg.transform.flip(self.img, self.activate, False), (self.rect.x, self.rect.y))
        if self.activated:
            textobj = self.font.render(self.text, 1, self.textcolor)
            textrect = textobj.get_rect()
            textrect.center = self.textlocation
            screen.blit(textobj, textrect)

class Movebox(Tile):
    def __init__(self, unscaled_x, unscaled_y, mapid):
        super(Movebox, self).__init__(unscaled_x, unscaled_y, 'movebox')
        self.mapid = mapid
        self.cooldown = False
        self.carried = False
        self.vertical_momentum = 0
        self.current_collision_type = {'top': False, 'bottom': False, 'right': False, 'left': False}

    def pickup(self, player):
        self.carried = True
        player.carrying = True
        player.bag = self
        self.cooldown = True
        self.rect.center = player.rect.center
        self.rect.bottom = player.rect.top

    def drop(self, player, impassable, movebox):
        temprect = self.rect.copy()
        if player.facing_left:
            temprect.right = player.rect.left
        else:
            temprect.left = player.rect.right

        tiles = impassable.copy()
        for box in movebox:
            if not movebox[box].carried and box != self.mapid:
                tiles[box] = movebox[box]
            else:
                tiles.pop(box, None)

        if len(self.collision_test(temprect, tiles)) == 0:
            self.rect = temprect
            self.carried = False
            player.carrying = False
            player.bag = None
            player.busy_box = 12
            self.cooldown = True

    def collision_test(self, rect, tiles):  # Public Domain by DaFluffyPotato
        hit_list = []
        for key in tiles:
            if rect.colliderect(tiles[key].rect):
                hit_list.append(tiles[key].rect)
        return hit_list

    def move(self, collision_types, rect, movement, tiles):  # Public Domain by DaFluffyPotato
        rect.y += movement[1]
        hit_list = self.collision_test(rect, tiles)
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
        return rect, collision_types

    def update(self, player, impassable, movebox):

        if self.rect.colliderect(player.rect_range1) and player.interact_pressed and not self.cooldown and not player.carrying and player.busy_box == 0:
            self.pickup(player)
        elif self.rect.colliderect(player.rect_range2) and player.interact_pressed and not self.cooldown and not player.carrying and player.busy_box == 0:
            self.pickup(player)
        elif self.carried and player.interact_pressed and not self.cooldown:
            self.drop(player, impassable, movebox)
        elif not player.interact_pressed and self.cooldown:
            self.cooldown = False

        if not self.carried:
            movement = [0, 0]

            movement[1] += self.vertical_momentum
            self.vertical_momentum += 1
            tiles = impassable.copy()
            for box in movebox:
                if not movebox[box].carried and box != self.mapid:
                    tiles[box] = movebox[box]
                else:
                    tiles.pop(box, None)
            tiles['player'] = player

            collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
            self.rect, self.current_collision_type = self.move(collision_types, self.rect, movement, tiles)

            if self.current_collision_type['bottom']:
                self.vertical_momentum = 0

    def draw(self, screen):
        screen.blit(self.img, (self.rect.x, self.rect.y))

class Redswitch(Tile):
    def __init__(self, unscaled_x, unscaled_y):
        super(Redswitch, self).__init__(unscaled_x, unscaled_y, 'redswitch')
        self.img_red = pg.image.load(config['game_spritepath'] + 'redswitch' + '.png').convert()
        self.img_green = pg.image.load(config['game_spritepath'] + 'greenswitch' + '.png').convert()
        self.img = self.img_red
        self.activated = False
        self.cooldown = False

    def toggle(self):
        if self.img == self.img_red:
            self.img = self.img_green
            self.activated = True
        else:
            self.img = self.img_red
            self.activated = False

    def update(self, player):
        if self.rect.colliderect(player.rect) and player.interact_pressed and not self.cooldown:
            self.toggle()
            self.cooldown = True
        if self.rect.colliderect(player.rect) and not player.interact_pressed:
            self.cooldown = False

    def draw(self, screen):
        screen.blit(self.img, (self.rect.x, self.rect.y))

class Barrier(Tile):
    def __init__(self, unscaled_x, unscaled_y, link):
        super(Barrier, self).__init__(unscaled_x, unscaled_y, 'ClosedBarrier')
        self.links = link
        self.img_closed = pg.image.load(config['game_spritepath'] + 'ClosedBarrier' + '.png').convert()
        self.img_open = pg.image.load(config['game_spritepath'] + 'OpenBarrier' + '.png').convert()
        self.img = self.img_closed
        self.opened = False
        self.activated = False
        self.barrier_sound = pg.mixer.Sound('sounds/doorsound.wav')
        self.barrier_sound.set_volume(0.5)

    def open(self):
        self.img = self.img_open
        self.activated = True
        self.barrier_sound.play()

    def close(self):
        self.img = self.img_closed
        self.activated = False
        self.barrier_sound.play()

    def update(self, map_logic, map_logic_table):
        self.activated = False
        for link in self.links:
            if map_logic[map_logic_table[link]].activated:
                self.activated = True
        if self.activated and not self.opened:
            self.opened = True
            self.open()
        elif not self.activated and self.opened:
            self.opened = False
            self.close()


    def draw(self, screen):
        screen.blit(self.img, (self.rect.x, self.rect.y))

class Plate(Tile):
    def __init__(self, unscaled_x, unscaled_y):
        super(Plate, self).__init__(unscaled_x, unscaled_y, 'plateup')

        self.img_platedown = pg.image.load(config['game_spritepath'] + 'platedown' + '.png').convert()
        self.img = self.img_platedown
        self.img_plateup = pg.image.load(config['game_spritepath'] + 'plateup' + '.png').convert()
        self.img_plateup.set_colorkey((255,255,255))

        self.rect = self.img_platedown.get_rect()
        self.rect.x = unscaled_x * config['game_tilesize']
        self.rect.y = unscaled_y * config['game_tilesize']

        self.rect_plate = self.img_plateup.get_rect()
        self.rect_plate.x = self.rect.x
        self.rect_plate.y = self.rect.y - 4
        self.activated = False

    def update(self, player, map_movebox):
        collide = False
        if self.rect_plate.colliderect(player.rect):
            collide = True
        for box in map_movebox:
            if self.rect_plate.colliderect(map_movebox[box].rect):
                collide = True
        if collide:
            self.activated = True
        else:
            self.activated = False

    def draw(self, screen):
        if self.activated:
            screen.blit(self.img, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.img_plateup, (self.rect_plate.x, self.rect_plate.y))

class Goal(Tile):
    def __init__(self, unscaled_x, unscaled_y):
        super(Goal, self).__init__(unscaled_x, unscaled_y, 'goal')

    def update(self, player):
        if self.rect.collidepoint(player.rect.center):
            return True
        else:
            return False

    def draw(self, screen):
        screen.blit(self.img, (self.rect.x, self.rect.y))

class Stage:
    def __init__(self, levelname):
        self.stage_data = self.load_stagedata(levelname)

        self.level_title = self.stage_data['level_name']
        self.level_name = levelname
        self.level_next = self.stage_data['next_level_name']
        self.playerspawn = (self.stage_data['player_spawn']['x'], self.stage_data['player_spawn']['y'])
        self.map_tiles = self.stage_data['map_data_impassable']
        self.map_helpbox = self.stage_data['map_data_helpbox']
        self.map_goal = self.stage_data['map_data_goal']
        self.map_movebox = self.stage_data['map_data_box']
        self.map_logic = self.stage_data['map_data_logic']
        self.map_logic_table = self.stage_data['map_data_logic_table']

        self.stage_finished = False

        self.time_font = pg.font.Font('freesansbold.ttf', 32)
        self.time_color = (0, 255, 0)
        self.time_location = (10, config['screen_height'] - 40)
        self.time_start = time.time()
        self.time_elap = 0

        self.name_font = pg.font.Font('freesansbold.ttf', 32)
        self.name_color = (0, 255, 0)
        self.name_location = (config['screen_width'] - 10, config['screen_height'] - 40)

    def load_stagedata(self, filename):
        try:
            path = './levels/' + filename + '.lvl'
            with open(path, 'r') as f:
                stage_data = yaml.safe_load(f)
        except FileNotFoundError as e:
            raise FileNotFoundError(filename)

        map_legend = stage_data['map_legend']

        map_data_raw = stage_data['map_data_raw'].split('\n')
        map_data_list = list()
        for row in map_data_raw:
            line = row.split(' ')
            data = list()
            for tile in line:
                data.append(int(tile))
            map_data_list.append(data)

        map_data_impassable = dict()
        map_data_helpbox = dict()
        map_data_goal = dict()
        map_data_box = dict()
        map_data_logic = dict()
        map_data_logic_table = dict()
        for y in range(len(map_data_list)):
            for x in range(len(map_data_list[y])):
                current_id = map_data_list[y][x]
                current_legendentry = map_legend[current_id]
                type = current_legendentry['type']
                if type in ['empty']:
                    pass
                elif type in ['helpbox']:
                    map_data_helpbox[str(x) + ';' + str(y)] = Helpbox(x, y, current_legendentry['text'])
                elif type in ['goal']:
                    map_data_goal[str(x) + ';' + str(y)] = Goal(x, y)
                elif type in ['movebox']:
                    map_data_box[str(x) + ';' + str(y)] = Movebox(x, y, str(x) + ';' + str(y))
                elif type in ['redswitch']:
                    map_data_logic[str(x) + ';' + str(y)] = Redswitch(x, y)
                    map_data_logic_table[current_id] = str(x) + ';' + str(y)
                elif type in ['ClosedBarrier']:
                    map_data_logic[str(x) + ';' + str(y)] = Barrier(x, y, current_legendentry['link'])
                    map_data_logic_table[current_id] = str(x) + ';' + str(y)
                elif type in ['plateup']:
                    map_data_logic[str(x) + ';' + str(y)] = Plate(x, y)
                    map_data_logic_table[current_id] = str(x) + ';' + str(y)
                else:
                    map_data_impassable[str(x) + ';' + str(y)] = Tile(x, y, type)

        stage_data['map_data_impassable']= map_data_impassable
        stage_data['map_data_helpbox'] = map_data_helpbox
        stage_data['map_data_goal'] = map_data_goal
        stage_data['map_data_box'] = map_data_box
        stage_data['map_data_logic'] = map_data_logic
        stage_data['map_data_logic_table'] = map_data_logic_table
        return stage_data

    def update(self, player):
        for tile in self.map_helpbox:
            self.map_helpbox[tile].update(player)
        for tile in self.map_movebox:
            self.map_movebox[tile].update(player, self.map_tiles, self.map_movebox)
        for tile in self.map_logic:
            if self.map_logic[tile].type in ['redswitch']:
                self.map_logic[tile].update(player)
            elif self.map_logic[tile].type in ['ClosedBarrier']:
                self.map_logic[tile].update(self.map_logic, self.map_logic_table)
            elif self.map_logic[tile].type in ['plateup']:
                self.map_logic[tile].update(player, self.map_movebox)
        for tile in self.map_goal:
            if self.map_goal[tile].update(player):
                self.stage_finished = True
        self.time_elap += time.time() - self.time_start
        self.time_start = time.time()

        return self.stage_finished

    def update_pause(self):
        self.time_start = time.time()

    def draw(self, screen):
        for tile in self.map_tiles:
            self.map_tiles[tile].draw(screen)
        for tile in self.map_helpbox:
            self.map_helpbox[tile].draw(screen)
        for tile in self.map_goal:
            self.map_goal[tile].draw(screen)
        for tile in self.map_movebox:
            self.map_movebox[tile].draw(screen)
        for tile in self.map_logic:
            self.map_logic[tile].draw(screen)

        if self.time_elap < 60:
            time_str = time.strftime("Time: %Ss", time.gmtime(self.time_elap))
        else:
            time_str = time.strftime("Time: %Mm %Ss", time.gmtime(self.time_elap))
        textobj = self.time_font.render(time_str, 1, self.time_color)
        textrect = textobj.get_rect()
        textrect.left = self.time_location[0]
        textrect.y = self.time_location[1]
        screen.blit(textobj, textrect)

        textobj = self.time_font.render("Level: " + self.level_title, 1, self.name_color)
        textrect = textobj.get_rect()
        textrect.right = self.name_location[0]
        textrect.y = self.name_location[1]
        screen.blit(textobj, textrect)

class Game_logic:

    def __init__(self, newgame=True):
        self.sf_window = pg.display.get_surface()
        self.sf_screen = pg.Surface((config['screen_width'], config['screen_height']))
        self.sf_screen_rect = self.sf_screen.get_rect()
        self.done = False
        self.clock = pg.time.Clock()
        self.framerate = config['framerate']
        self.keys = pg.key.get_pressed()

        # self.music_bg = pg.mixer.music.load('./sounds/BGM.wav')
        # pg.mixer.music.play(-1)
        # pg.mixer.music.set_volume(0.4)

        if newgame:
            self.stage_current = "level1"
        else:
            self.stage_current = self.loadsavefile()
        self.stage = Stage(self.stage_current)

        self.player = Player()
        self.player.teleport(self.stage.playerspawn)

        self.stage_resetted = False
        self.stage_finished = False

        self.paused_pressed = False
        self.paused = False
        self.pause_font_color = (255, 255, 255)
        self.paused_font_1 = pg.font.Font('freesansbold.ttf', 50)
        self.pause_location_1 = (config['screen_width']/2, config['screen_height']/3)
        self.paused_font_2 = pg.font.Font('freesansbold.ttf', 30)
        self.pause_location_2 = (config['screen_width']/2, config['screen_height']/2)

        self.saving_game = False

    def reset_stage(self):
        oldtimer = self.stage.time_elap
        self.stage = Stage(self.stage_current)

        self.stage.time_elap += oldtimer
        self.player = Player()
        self.player.teleport(self.stage.playerspawn)

    def loadsavefile(self):
        try:
            path = 'save.box'
            with open(path, 'r') as f:
                save = yaml.safe_load(f)
            return save['savedlevel']
        except FileNotFoundError as e:
            print('Error: No save file found. Starting new game')
            return 'level1'

    def savegame(self):
        savedlevel = self.stage.level_name
        saveboxfile = Path("save.box")
        if saveboxfile.is_file(): # save.box exist
            try:
                with open(saveboxfile, 'r') as f:
                    save = yaml.safe_load(f)
                save['savedlevel'] = savedlevel
            except TypeError:
                save = dict(savedlevel=savedlevel)
            with open(saveboxfile, 'w') as outfile:
                yaml.dump(save, outfile, default_flow_style=False)
        else: # save.box doesnot exist. create it
            data = dict(savedlevel=savedlevel)
            with open(saveboxfile, 'w') as outfile:
                yaml.dump(data, outfile, default_flow_style=False)

    def event_loop(self):
        for event in pg.event.get():
            self.keys = pg.key.get_pressed()
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                pass
            if event.type == pg.KEYUP:
                if event.key in [pg.K_ESCAPE, pg.K_c]:
                    self.paused_pressed = False
                if event.key in [pg.K_s]:
                    self.saving_game = False
            if self.paused:
                if event.type == pg.KEYDOWN:
                    if event.key in [pg.K_ESCAPE, pg.K_c]:
                        if not self.paused_pressed:
                            self.paused = not self.paused
                            self.paused_pressed = True
                    if event.key in [pg.K_q]:
                        pg.quit()
                        sys.exit()
                    if event.key in [pg.K_s]:
                        if not self.saving_game:
                            self.savegame()
                            self.saving_game = True
                self.player.get_event_always(event)
            else:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        if not self.stage_resetted:
                            self.reset_stage()
                            self.stage_resetted = True
                    if event.key == pg.K_ESCAPE:
                        if not self.paused_pressed:
                            self.paused = not self.paused
                            self.paused_pressed = True
                if event.type == pg.KEYUP:
                    if event.key == pg.K_r:
                        self.stage_resetted = False
                self.player.get_event(event)

    def update(self):
        if not self.paused:
            self.player.update(self.stage.map_tiles, self.stage.map_logic, self.stage.map_movebox)
            self.stage_finished = self.stage.update(self.player)
        else:
            self.stage.update_pause()

        if self.stage_finished:
            self.stage_current = self.stage.level_next

        if self.stage_current == "GAMEOVER":
            self.done = True
        elif self.stage_finished:
            self.stage_finished = False
            self.reset_stage()

    def draw(self):
        self.sf_screen.fill(config['color_backgroud'])

        self.stage.draw(self.sf_screen)
        self.player.draw(self.sf_screen)

        if self.paused:

            textobj = self.paused_font_1.render("Game Paused!", 1, self.pause_font_color)
            textrect = textobj.get_rect()
            textrect.center = self.pause_location_1
            pg.draw.rect(self.sf_screen, (102, 102, 102), textrect.inflate(20, 20))
            self.sf_screen.blit(textobj, textrect)


            textobj = self.paused_font_2.render("Press 'C' to Continue, 'S' to save, or 'Q' to Quit", 1, self.pause_font_color)
            textrect = textobj.get_rect()
            textrect.center = self.pause_location_2
            pg.draw.rect(self.sf_screen, (102, 102, 102), textrect.inflate(20, 20))
            self.sf_screen.blit(textobj, textrect)


        self.sf_window.blit(pg.transform.scale(self.sf_screen, self.sf_window.get_size()), (0, 0))

    def display_fps(self):
        caption = "{} - FPS: {:.2f}".format(config['window_caption'], self.clock.get_fps())
        pg.display.set_caption(caption)

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.update()
            self.draw()
            pg.display.update()
            self.clock.tick(self.framerate)
            self.display_fps()

def start():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.mixer.pre_init(22050, -16, 2, 512)
    pg.init()
    pg.mixer.set_num_channels(64)
    pg.font.init()

    pg.display.set_caption(config['window_caption'])
    pg.display.set_icon(pg.image.load("sprites/icon.jpg"))
    pg.display.set_mode((config['window_width'], config['window_height']), 0, 32)

    intro = Game_intro()
    next = intro.main_loop()

    if next in ['start']:
        game = Game_logic()
        game.main_loop()
    elif next in ['continue']:
        game = Game_logic(newgame=False)
        game.main_loop()

    gameover = Game_over()
    gameover.main_loop()

    pg.quit()
    sys.exit()

if __name__ == '__main__':
    start()
