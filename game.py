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
import pygame as pg
import yaml


config = {
     'window_width': 1280
    ,'window_height': 720
    ,'screen_width': 1280
    ,'screen_height': 720
    ,'framerate': 60.0
    ,'window_caption': 'Puzzle Game'
    ,'color_backgroud': (24, 20, 37, 1)
    ,'intro_backImg': 'background.jpg'
    ,'intro_backcolor': (56, 142, 142)
    ,'intro_buttontextcolor': (0, 0, 0)
    ,'intro_startcolor_ic': (0, 200, 0)
    ,'intro_startcolor_ac': (0, 255, 0)
    ,'intro_continuecolor_ic': (0, 0, 100)
    ,'intro_continuecolor_ac': (0, 0, 255)
    ,'intro_quitcolor_ic': (200, 0, 0)
    ,'intro_quitcolor_ac': (255, 0, 0)
    ,'game_characterpath': "./characters/"
    ,'game_spritepath': "./sprites/"
    ,'game_tilesize': 24
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
        self.button_start = self.Button("Start", 600, 450, 100, 50, config['intro_startcolor_ic'], config['intro_startcolor_ac'])
        self.button_continue = self.Button("Continue", 600, 550, 100, 50, config['intro_continuecolor_ic'], config['intro_continuecolor_ac'])
        self.button_quit = self.Button("Quit", 600, 650, 100, 50, config['intro_quitcolor_ic'], config['intro_quitcolor_ac'])

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
            self.textcolor = config['intro_buttontextcolor']

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
                self.done = True
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
        self.sf_screen.fill(config['intro_backcolor'])
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

class Player:
    def __init__(self):
        self.img_jill = pg.image.load(config['game_characterpath'] + "Jill/Right.gif").convert()
        self.img_jack = pg.image.load(config['game_characterpath'] + "Jack/Right.gif").convert()
        self.img = self.img_jill
        self.rect = self.img.get_rect()
        self.moving_left = False
        self.moving_right = False
        self.moving_jumping = False
        self.facing_left = False
        self.carrying = False
        # self.telported = False

    def move_force(self, location):
        self.rect.x = location[0]
        self.rect.y = location[1]

    def event_loop(self):
        pass

    def update(self):
        pass

    def draw(self,screen):
        screen.blit(self.img, (self.rect.x, self.rect.y))

class Tile:
    def __init__(self, type, unscaled_x, unscaled_y):
        self.type = type
        self.img = pg.image.load(config['game_spritepath'] + self.type + '.png').convert()
        self.rect = self.img.get_rect()
        self.rect.x = unscaled_x * config['game_tilesize']
        self.rect.y = unscaled_y * config['game_tilesize']

    # def event_loop(self):
    #     pass

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.img, (self.rect.x, self.rect.y))

class Stage:
    def __init__(self, levelname):
        self.stage_data = self.load_stagedata(levelname)
        self.level_name = self.stage_data['level_name']
        self.level_next = self.stage_data['next_level_name']

        self.playerspawn = (self.stage_data['player_spawn']['x'], self.stage_data['player_spawn']['y'])
        self.map_data = self.stage_data['map_data']


    def load_stagedata(self, filename):
        path = './levels/' + filename + '.lvl'
        with open(path) as f:
            stage_data = yaml.safe_load(f)

        map_legend = stage_data['map_legend']
        # map_links = stage_data['map_links']
        map_data_raw = stage_data['map_data_raw'].split('\n')
        map_data_list = list()
        for row in map_data_raw:
            line = row.split(' ')
            data = list()
            for tile in line:
                data.append(int(tile))
            map_data_list.append(data)

        map_data = dict()
        for y in range(len(map_data_list)):
            for x in range(len(map_data_list[y])):
                type = map_legend[map_data_list[y][x]]['type']
                # print(type)
                if type in ['wall', 'floor', 'goal', 'helpbox']:
                    map_data[str(x) + ';' + str(y)] = Tile(type, x, y)
        stage_data['map_data']= map_data
        return stage_data

    # def event_loop(self):
    #     pass

    def update(self):
        pass

    def draw(self, screen):
        for tile in self.map_data:
            self.map_data[tile].draw(screen)

class Game_logic:

    def __init__(self, newgame=True):
        self.sf_window = pg.display.get_surface()
        self.sf_screen = pg.Surface((config['screen_width'], config['screen_height']))
        self.sf_screen_rect = self.sf_screen.get_rect()
        self.done = False
        self.clock = pg.time.Clock()
        self.framerate = config['framerate']
        self.keys = pg.key.get_pressed()

        if newgame:
            self.stage_current = "level1"
        else:
            self.stage_current = "level1" # TODO in future load save
        self.stage = Stage(self.stage_current)

        self.player = Player()
        self.player.move_force(self.stage.playerspawn)


    def event_loop(self):
        for event in pg.event.get():
            self.keys = pg.key.get_pressed()
            if event.type == pg.QUIT:
                self.done = True

    def update(self):
        pass

    def draw(self):
        self.sf_screen.fill(config['color_backgroud'])

        self.stage.draw(self.sf_screen)
        self.player.draw(self.sf_screen)

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
    pg.display.set_icon(pg.image.load("./sprites/icon.jpg"))
    pg.display.set_mode((config['window_width'], config['window_height']), 0, 32)

    intro = Game_intro()
    next = intro.main_loop()

    if next in ['start']:
        game = Game_logic()
        game.main_loop()
    elif next in ['continue']:
        game = Game_logic(newgame=False)
        game.main_loop()

    pg.quit()
    sys.exit()

if __name__ == '__main__':
    start()
