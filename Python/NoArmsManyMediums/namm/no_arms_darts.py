"""

No Arms Darts

    Copyright (C) 2014  Tim Kracht <timkracht4@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


import os
import pygame
import time

from namm.common.logger import Logger
from namm.common import menu
from namm.intro import namm_intro
from namm.darts import dartboarduino
from namm.Games import get_game_list, get_game

ST_INTRO = "Intro"
ST_GAMES = "Games"
ST_LOADING = "Loading"
ST_CONNECTING = "Connecting"
ST_CONNECTED = "Connected"
ST_ERROR_CONNECTING = "Connection Error"
ST_MAIN = "Main"
ST_GAME_MENU = "Game Menu"
ST_PLAY_GAME = "PlayGame"
ST_BACK = "Back"
ST_LEFT = "Left"
ST_RIGHT = "Right"
ST_QUIT = "Quit"


# TODO: private and properties, more logging and menu instance
class NoArmsDarts(object):
    def __init__(self, screen, log_level="Warn"):
        if not os.path.exists("log"):
            os.mkdir("log")
        self._logger = Logger(log_level, os.path.join("log", "NoArmsDarts.log"))
        self._logger.start()

        self._logger.log("Info", "Started Logging.")
        # self.screen_size = (640, 480)
        # self.screen_depth = screen.get_bitsize()
        self._screen = screen
        # self.screen = pygame.Surface(self.screen_size, 0, self.screen_depth)

        self._state = ST_INTRO
        self._game = None

        # menus
        self._menu = None
        self._menu_bg_image = None
        self._menu_font = None

        # backgrounds
        # self._connected_bg = pygame.image.load(os.path.join('namm', 'images', 'naDarts', 'images',
        #                                                         'hireswallpaperboardgreenpredator.png')).convert()
        self._connected_bg = pygame.image.load(os.path.join('namm', 'images', 'naDarts', 'images',
                                                            'GreenBackground.png')).convert()
        self._disconnected_bg = pygame.image.load(os.path.join('namm', 'images', 'naDarts', 'images',
                                                               'OrangeBackground.png')).convert()

        self._logger.log("Debug", "Instantiating Dartboarduino...")
        self._dartboard = dartboarduino.Dartboarduino(log_level, autoconnect=False)
        
        self._logger.log("Info", "Pygame display set.")

    def run(self):
        try:
            self._logger.log("Debug", "Entering run()")
            self._logger.log("Debug", "State: " + self._state)

            self._menu_bg_image = pygame.transform.scale(self._disconnected_bg, (self._screen.get_rect().width,
                                                                                 self._screen.get_rect().height))
            self._menu_font = os.path.join('namm', 'fonts', 'FAKERECE.TTF')
            # self.menuFont = os.path.join('namm', 'fonts','256BYTES.ttf')

            self._build_menu()

            while self._state != ST_QUIT:
                if self._state == ST_INTRO:
                    self._show_intro()
                    self._state = ST_CONNECTING
                elif self._state == ST_CONNECTING:
                    self._menu_bg_image = pygame.transform.scale(self._disconnected_bg, (self._screen.get_rect().width,
                                                                                         self._screen.get_rect().height)
                                                                 )
                    self._menu.background(self._menu_bg_image)
                    self._menu.page_id = ST_CONNECTING
                    self._menu.get_action(menu.PAGE_ACTION_NO_ACTION)
                    if self._dartboard.reconnect():
                        self._dartboard.connect()
                        if self._dartboard.state == "Stopped":
                            self._menu_bg_image = pygame.transform.scale(self._connected_bg, (self._screen.get_rect().width,
                                                                                 self._screen.get_rect().height))
                            self._menu.background(self._menu_bg_image)
                            self._menu.page_id = ST_CONNECTED
                            self._menu.get_action(menu.PAGE_ACTION_NO_ACTION)
                            time.sleep(2)
                            self._state = ST_MAIN
                    if self._state == ST_CONNECTING:
                        time.sleep(2)
                        self._menu.page_id = ST_ERROR_CONNECTING
                        if self._menu.get_action() == menu.PAGE_ACTION_MAIN:
                            self._state = ST_MAIN
                elif self._state == ST_MAIN:
                    self._menu.page_id = ST_MAIN
                    selection = self._menu.get_action()
                    if selection not in (ST_RIGHT, ST_LEFT):  # TODO
                        self._state = selection
                elif self._state == ST_GAMES:
                    self._menu.page_id = ST_GAMES
                    selection = self._menu.get_action()
                    if selection in (ST_BACK, ST_LEFT, ST_QUIT):
                        self._state = ST_MAIN
                    elif selection != ST_RIGHT:
                        self._menu.page_id = ST_LOADING
                        no_action = self._menu.get_action(menu.PAGE_ACTION_NO_ACTION)
                        self._game = get_game(selection)
                        self._state = ST_GAME_MENU
                elif self._state == ST_GAME_MENU:
                    game_menu = self._game.game_menu(self._screen, self._menu_bg_image, self._menu_font,
                                                     self._logger.log_level)
                    action = game_menu.get_action()
                    if action == menu.PAGE_ACTION_GO:
                        self._state = ST_PLAY_GAME
                    elif action == menu.PAGE_ACTION_QUIT:
                        self._state = ST_QUIT
                    else:
                        self._state = ST_GAMES
                elif self._state == ST_PLAY_GAME:
                    self._logger.log("Debug", "Play Game!")

                    while self._state == ST_PLAY_GAME:
                        if self._dartboard.state == "Stopped":
                            self._dartboard.play()
                            if self._dartboard.state == "Playing":
                                self._state = ST_MAIN

                        else:
                            self._menu_bg_image = pygame.transform.scale(self._disconnected_bg,
                                                                         (self._screen.get_rect().width,
                                                                          self._screen.get_rect().height))
                            self._menu.background(self._menu_bg_image)
                            self._menu.page_id = ST_CONNECTING
                            self._menu.get_action(menu.PAGE_ACTION_NO_ACTION)
                            self._dartboard.disconnect()
                            if self._dartboard.reconnect():
                                self._dartboard.connect()
                                if self._dartboard.state == "Stopped":
                                    self._menu_bg_image = pygame.transform.scale(self._connected_bg,
                                                                                 (self._screen.get_rect().width,
                                                                                  self._screen.get_rect().height))
                                    self._menu.background(self._menu_bg_image)
                                    self._menu.page_id = ST_CONNECTED
                                    self._menu.get_action(menu.PAGE_ACTION_NO_ACTION)
                                    self._dartboard.play()
                                    if self._dartboard.state == "Playing":
                                        self._state = ST_MAIN
                                    else:
                                        self._menu_bg_image = pygame.transform.scale(self._disconnected_bg,
                                                                         (self._screen.get_rect().width,
                                                                          self._screen.get_rect().height))
                                        self._menu.background(self._menu_bg_image)

                        if self._state == ST_PLAY_GAME:
                            time.sleep(2)
                            self._menu.page_id = ST_ERROR_CONNECTING
                            if self._menu.get_action() == menu.PAGE_ACTION_MAIN:
                                self._state = ST_MAIN
                else:
                    self._logger.log("Error", "Unknown Menu State: " + self._state)
                    self._state = ST_MAIN  # TODO: ?

            self._logger.log("Debug", "Exiting run()")
        except Exception, e:
            if self._logger:
                self._logger.log("Error", e.message)
                self._logger.log("Error", e.args)
            else:
                print e
        finally:
            if self._logger:
                self._logger.stop()

    def _show_intro(self):
        self._logger.log("Debug", "Entering show_intro()")
        intro = namm_intro.NammIntro(self._screen)
        intro.run()
        intro = None
        self._logger.log("Debug", "Exiting show_intro()")

    def _build_menu(self):
        self._logger.log("Debug", "Entering _build_menu()")
        self._menu = menu.Menu()
        self._menu.add_page(self._main_page(ST_MAIN))
        self._menu.add_page(self._games_page(ST_GAMES))
        self._menu.add_page(self._loading_page(ST_LOADING))
        self._menu.add_page(self._connecting_page(ST_CONNECTING))
        self._menu.add_page(self._connected_page(ST_CONNECTED))
        self._menu.add_page(self._could_not_connect_page(ST_ERROR_CONNECTING))

    def _main_page(self, id):
        self._logger.log("Debug", "Entering _main_page()")
        menu_items = ((menu.MENU_ITEM_RENDER_BLANK, None, None),
                      (menu.MENU_ITEM_RENDER_NORMAL, 'Replay Intro', ST_INTRO),
                      (menu.MENU_ITEM_RENDER_NORMAL, 'Games', ST_GAMES),
                      (menu.MENU_ITEM_RENDER_BLANK, None, None),
                      (menu.MENU_ITEM_RENDER_NORMAL, 'Quit', ST_QUIT))
        header = "Main Menu"
        font_size = 72  # int(math.ceil(self.display_screen.get_rect().height / (len(menu_items) + 3)))
        return menu.MenuPage(id, self._screen, menu_items, header, (0, 0, 0), self._menu_bg_image,
                             self._menu_font, font_size)

    def _games_page(self, id):
        self._logger.log("Debug", "Entering _games_page()")
        menu_items = [(menu.MENU_ITEM_RENDER_BLANK, None, None)]
        for game in get_game_list():
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, game, game))
        header = "Games"
        font_size = 72  # int(math.ceil(self.display_screen.get_rect().height / (len(menu_items) + 3)))
        return menu.MenuPage(id, self._screen, menu_items, header, (0, 0, 0), self._menu_bg_image, self._menu_font,
                             font_size, nav_back=ST_BACK)

    def _loading_page(self, id):
        self._logger.log("Debug", "Entering _loading_page()")
        menu_items = ((menu.MENU_ITEM_RENDER_BLANK, None, None),
                      (menu.MENU_ITEM_RENDER_BLANK, None, None),
                      (menu.MENU_ITEM_RENDER_NORMAL, '   Game Loading...', None))
        header = ""
        font_size = 72  # int(math.ceil(self.display_screen.get_rect().height / (len(menu_items) + 3)))
        return menu.MenuPage(id, self._screen, menu_items, header, (0, 0, 0), self._menu_bg_image, self._menu_font,
                             font_size)

    def _connecting_page(self, id):
        self._logger.log("Debug", "Entering _connecting_page()")
        menu_items = ((menu.MENU_ITEM_RENDER_BLANK, None, None),
                      (menu.MENU_ITEM_RENDER_BLANK, None, None),
                      (menu.MENU_ITEM_RENDER_NORMAL, '  Connecting to Dartboard...', None))
        header = ""
        font_size = 72  # int(math.ceil(self.display_screen.get_rect().height / (len(menu_items) + 3)))
        return menu.MenuPage(id, self._screen, menu_items, header, (0, 0, 0), self._menu_bg_image, self._menu_font,
                             font_size)

    def _connected_page(self, id):
        self._logger.log("Debug", "Entering _connected_page()")
        menu_items = ((menu.MENU_ITEM_RENDER_BLANK, None, None),
                      (menu.MENU_ITEM_RENDER_BLANK, None, None),
                      (menu.MENU_ITEM_RENDER_NORMAL, 'Connected to Dartboard!', None))
        header = ""
        font_size = 72  # int(math.ceil(self.display_screen.get_rect().height / (len(menu_items) + 3)))
        return menu.MenuPage(id, self._screen, menu_items, header, (0, 0, 0), self._menu_bg_image, self._menu_font,
                             font_size)

    def _could_not_connect_page(self, id):
        self._logger.log("Debug", "Entering _could_not_connect_page()")
        menu_items = ((menu.MENU_ITEM_RENDER_BLANK, None, None),
                      (menu.MENU_ITEM_RENDER_NORMAL, 'Could not connect to the dartboard!', None),
                      (menu.MENU_ITEM_RENDER_NORMAL, 'Try Again', menu.PAGE_ACTION_NEXT))
        header = "Not Good"
        font_size = 48  # int(math.ceil(self.display_screen.get_rect().height / (len(menu_items) + 3)))
        return menu.MenuPage(id, self._screen, menu_items, header, (0, 0, 0), self._menu_bg_image, self._menu_font,
                             font_size, nav_main=menu.PAGE_ACTION_MAIN)
