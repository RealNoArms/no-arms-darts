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

import math
import os
import pygame
import sys

from pygame.locals import *

from namm.common import *
from namm.intro import *
from namm.darts import *
from namm.Games import *
from namm.Games import get_game_list, get_game


class NoArmsDarts():
    def __init__(self, screen, log_level="Warn"):
        if not os.path.exists("log"):
            os.mkdir("log")
        self.logger = utilities.Logger(log_level, os.path.join("log", "NoArmsDarts.log"))
        self.logger.start()

        self.logger.log("Info", "Started Logging.")
        # self.screen_size = (640, 480)
        # self.screen_depth = screen.get_bitsize()
        self.display_screen = screen
        # self.screen = pygame.Surface(self.screen_size, 0, self.screen_depth)

        self.state = "Intro"
        self.current_game = None

        # menus
        self.mainMenu = None
        self.gamesMenu = None
        self.gameMainMenu = None
        self.gameInstrMenu = None
        self.gameInstrMainMenu = None
        self.selVariationMenu = None
        self.selPlayersMenu = None
        self.menuBgImage = None
        self.menuFont = None
        
        self.logger.log("Info", "Pygame display set.")

    def run(self):
        try:
            self.logger.log("Debug", "Entering Run()")
            self.logger.log("Debug", "State: " + self.state)

            self.menuBgImage = pygame.image.load(os.path.join('namm', 'images', 'naDarts', 'images',
                                                              'hireswallpaperboardgreenpredator.png')).convert()
            self.menuBgImage = pygame.transform.scale(self.menuBgImage, (self.display_screen.get_rect().width,
                                                                         self.display_screen.get_rect().height))
            self.menuFont = os.path.join('namm', 'fonts', 'FAKERECE.TTF')
            # self.menuFont = os.path.join('namm', 'fonts','256BYTES.ttf')

            self.mainMenu = self.get_main_menu()
            self.mainMenu.bg_image = self.menuBgImage
            self.gamesMenu = self.get_games_menu()
            self.gamesMenu.bg_image = self.menuBgImage
            instr_page_number = 1
            
            while self.state != 'Quit':
                if self.state == 'Intro':
                    self.show_intro()
                    self.state = 'Main'
                elif self.state == 'Main':
                    selection = self.mainMenu.get_action()
                    if selection not in ('Right', 'Left'):
                        self.state = selection
                elif self.state == 'Games':
                    selection = self.gamesMenu.get_action()
                    if selection in ('Back', 'Left'):
                        self.state = 'Main'
                    elif selection != 'Right':
                        self.current_game = get_game(selection)
                        self.state = 'GameMain'
                elif self.state == 'GameMain':
                    self.gameMainMenu = self.get_game_main_menu('Games')
                    self.gameMainMenu.bg_image = self.menuBgImage
                    selection = self.gameMainMenu.get_action()
                    if selection == 'Left':
                        self.state = 'Games'
                    elif selection != 'Right':
                        self.state = selection
                elif self.state == 'GameInstr':
                    max_page = 5
                    self.gameInstrMainMenu = self.get_game_instr_menu('GameMain', instr_page_number)
                    self.gameInstrMainMenu.bg_image = self.menuBgImage
                    selection = self.gameInstrMainMenu.get_action()
                    if (selection == 'GameMain' or
                            (selection == 'Right' and instr_page_number == max_page) or
                            (selection == 'Left' and instr_page_number == 1)):
                        instr_page_number = 1
                        self.state = 'GameMain'
                    elif selection == 'Left':
                        instr_page_number -= 1
                    elif selection == 'Right':
                        instr_page_number += 1
                    else:
                        instr_page_number = int(selection)
                elif self.state == 'SelPlayers':
                    self.selPlayersMenu = self.get_select_players_menu()
                    self.selPlayersMenu.bg_image = self.menuBgImage
                    selection = self.selPlayersMenu.get_action()
                    if selection == 'Left':
                        self.state = 'GameMain'
                    elif selection != 'Right':
                        players = []
                        for i in range(1, int(selection)+1):
                            players.append(Darts.Player("Player {0}".format(i)))
                        self.current_game.players = players
                        # print self.current_game.players
                        self.state = 'SelVariation'
                elif self.state == 'SelVariation':
                    self.selVariationMenu = self.get_select_variation_menu()
                    self.selVariationMenu.bg_image = self.menuBgImage
                    selection = self.selVariationMenu.get_action()
                    if selection == 'Left':
                        self.state = 'SelPlayers'
                    elif selection != 'Right':
                        self.current_game.variation = selection
                        self.state = 'SelVariation'  # SelGoal??? Points versus rounds
            self.logger.log("Debug", "Exiting Run()")
        except Exception, e:
            print e
        finally:
            self.logger.stop()

    def show_intro(self):
        self.logger.log("Debug", "Entering ShowIntro()")
        intro = nammIntro.NammIntro(self.display_screen)
        intro.Run()
        intro = None
        self.logger.log("Debug", "Exiting ShowIntro()")

    def get_main_menu(self):
        self.logger.log("Debug", "Entering MainMenu()")
        menu_items = ((menu.MENU_ITEM_RENDER_BLANK, None, None),
                      (menu.MENU_ITEM_RENDER_NORMAL, 'Replay Intro', 'Intro'),
                      (menu.MENU_ITEM_RENDER_NORMAL, 'Games', 'Games'),
                      (menu.MENU_ITEM_RENDER_BLANK, None, None),
                      (menu.MENU_ITEM_RENDER_NORMAL, 'Quit', 'Quit'))
        header = "Main Menu"
        font_size = 72  # int(math.ceil(self.display_screen.get_rect().height / (len(menu_items) + 3)))
        main_menu = menu.GameMenu(self.display_screen, menu_items, header, (0, 0, 0), self.menuFont, font_size)

        return main_menu

        # self.state = mainMenu.get_action()
        # self.logger.log("Debug","State: " + self.state)
        # self.logger.log("Debug","Exiting MainMenu()")

    def get_games_menu(self):
        self.logger.log("Debug", "Entering GamesMenu()")
        menu_items = [(menu.MENU_ITEM_RENDER_BLANK, None, None)]
        for game in get_game_list():
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, game, game))
        menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))
        menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Back', 'Back'))
        header = "Games"
        font_size = 72  # int(math.ceil(self.display_screen.get_rect().height / (len(menu_items) + 3)))
        games_menu = menu.GameMenu(self.display_screen, menu_items, header, (0, 0, 0), self.menuFont, font_size)

        return games_menu
        '''selection = gamesMenu.get_action()
        self.logger.log("Debug","Selection: " + selection)
        if selection == "Back":
            self.state = "Main"
        else:
            self.current_game = get_game(selection)
            self.state = "GameMain"
        self.logger.log("Debug","Exiting GamesMenu()")'''

    def get_select_variation_menu(self):
        self.logger.log("Debug", "Entering SelectVariationMenu()")
        menu_items = [(menu.MENU_ITEM_RENDER_BLANK, None, None)]
        for line in self.current_game._variationOptions:  # TODO: make variation options property
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, line, line))
        menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))
        menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Back', 'Left'))
        header = "Select Game Variation"
        font_size = 64  # int(math.ceil(self.display_screen.get_rect().height / (len(menu_items) + 3)))
        sel_variation_menu = menu.GameMenu(self.display_screen, menu_items, header, (0, 0, 0), self.menuFont, font_size)

        return sel_variation_menu

    def get_select_players_menu(self):
        self.logger.log("Debug", "Entering SelectPlayersMenu()")
        menu_items = [(menu.MENU_ITEM_RENDER_BLANK, None, None)]
        for option in self.current_game._playerOptions:  # TODO: make player options property
            if option == 1:
                line = str(option) + ' Player'
            else:
                line = str(option) + ' Players'
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, line, str(option)))
        menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))
        menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Back', 'Left'))
        header = "Select Number of Players"
        font_size = 48  # int(math.ceil(self.display_screen.get_rect().height / (len(menu_items) + 3)))
        sel_players_menu = menu.GameMenu(self.display_screen, menu_items, header, (0, 0, 0), self.menuFont, font_size)

        return sel_players_menu

    def get_game_main_menu(self, prev_state):
        self.logger.log("Debug", "Entering GameMainMenu()")
        menu_items = ((menu.MENU_ITEM_RENDER_BLANK, None, None),
                      (menu.MENU_ITEM_RENDER_NORMAL, 'Instructions', 'GameInstr'),
                      (menu.MENU_ITEM_RENDER_NORMAL, 'High Scores', 'GameMain'),
                      (menu.MENU_ITEM_RENDER_NORMAL, 'Play', 'SelPlayers'),
                      (menu.MENU_ITEM_RENDER_BLANK, None, None),
                      (menu.MENU_ITEM_RENDER_NORMAL, 'Back', prev_state))
        header = self.current_game.name
        font_size = 72  # int(math.ceil(self.display_screen.get_rect().height / (len(menu_items) + 3)))
        game_main_menu = menu.GameMenu(self.display_screen, menu_items, header, (0, 0, 0), self.menuFont, font_size)

        return game_main_menu
        # self.state = gameMainMenu.get_action()
        # self.logger.log("Debug","State: " + self.state)
        # self.logger.log("Debug","Exiting GameMainMenu()")

    def get_game_instr_menu(self, prev_state, page_number):
        self.logger.log("Debug", "Entering GameInstrMenu()")
        max_width = self.display_screen.get_rect().width - 20
        menu_items = []
        # menu_items.append((menu.MENU_ITEM_RENDER_BLANK,None,None))

        if page_number == 1:
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Summary:', None))
            menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))
    
            for line in self.current_game.instructions[Darts.INSTR_SUMMARY]:
                menu_items.append((menu.MENU_ITEM_RENDER_WRAP, line, None, max_width))

            menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Next', '2'))
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Back', prev_state))

        elif page_number == 2:
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Object:', None))
            menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))

            for line in self.current_game.instructions[Darts.INSTR_OBJECT]:
                menu_items.append((menu.MENU_ITEM_RENDER_WRAP, line, None, max_width))

            menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Next', '3'))
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Back', '1'))

        elif page_number == 3:
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Game Play:', None))
            menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))

            for line in self.current_game.instructions[Darts.INSTR_GAMEPLAY]:
                menu_items.append((menu.MENU_ITEM_RENDER_WRAP, line, None, max_width))

            menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Next', '4'))
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Back', '2'))

        elif page_number == 4:
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Scoring:', None))
            menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))

            for line in self.current_game.instructions[Darts.INSTR_SCORING]:
                menu_items.append((menu.MENU_ITEM_RENDER_WRAP, line, None, max_width))

            menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Next', '5'))
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Back', '3'))

        elif page_number == 5:
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Variations:', None))
            menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))

            for line in self.current_game.instructions[Darts.INSTR_VARIATIONS]:
                menu_items.append((menu.MENU_ITEM_RENDER_WRAP, line, None, max_width))

            menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Back', '4'))
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Done', prev_state))

        header = self.current_game.name
        font_size = 36  # int(math.ceil(self.display_screen.get_rect().height / (len(menu_items) + 3)))
        game_instr_menu = menu.GameMenu(self.display_screen, menu_items, header, (0, 0, 0), self.menuFont, font_size)

        return game_instr_menu
