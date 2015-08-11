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

ST_INTRO = "Intro"
ST_GAMES = "Games"
ST_MAIN = "Main"
ST_GAME_MAIN = "GameMain"
ST_GAME_INSTR = "GameInstr"
ST_SEL_PLAYERS = "SelPlayers"
ST_SEL_VARIATION = "SelVariation"
ST_SEL_SETTINGS = "SelSettings"
ST_SHOW_SUMMARY = "ShowSummary"
ST_PLAY_GAME = "PlayGame"
ST_BACK = "Back"
ST_LEFT = "Left"
ST_RIGHT = "Right"
ST_QUIT = "Quit"

# TODO: private and properties, more logging
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

        self.state = ST_INTRO
        self.current_game = None

        # menus
        self.mainMenu = None
        self.gamesMenu = None
        self.gameMainMenu = None
        # self.gameInstrMenu = None
        self.gameInstrMainMenu = None
        self.selVariationMenu = None
        self.selPlayersMenu = None
        self.selSettingsMenu = None
        self.summaryMenu = None
        self.menuBgImage = None
        self.menuFont = None

        self.logger.log("Debug", "Instantiating Dartboarduino...")
        self.dartboard = Dartboarduino.Dartboarduino(log_level, autoconnect=False)
        
        self.logger.log("Info", "Pygame display set.")

    def run(self):
        try:
            self.logger.log("Debug", "Entering run()")
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
            
            while self.state != ST_QUIT:
                if self.state == ST_INTRO:
                    self.show_intro()
                    self.state = ST_MAIN
                elif self.state == ST_MAIN:
                    selection = self.mainMenu.get_action()
                    if selection not in (ST_RIGHT, ST_LEFT):
                        self.state = selection
                elif self.state == ST_GAMES:
                    selection = self.gamesMenu.get_action()
                    if selection in (ST_BACK, ST_LEFT, ST_QUIT):
                        self.state = self.gamesMenu.prev_state
                    elif selection != ST_RIGHT:
                        self.current_game = get_game(selection)
                        self.state = self.gamesMenu.next_state
                elif self.state == ST_GAME_MAIN:
                    if self.gameMainMenu is None:
                        self.gameMainMenu = self.get_game_main_menu(ST_GAMES)
                        self.gameMainMenu.bg_image = self.menuBgImage

                    self.gameInstrMainMenu = None
                    self.selVariationMenu = None
                    self.selPlayersMenu = None
                    self.selSettingsMenu = None
                    self.summaryMenu = None
                    
                    selection = self.gameMainMenu.get_action()
                    if selection == ST_LEFT:
                        self.state = self.gameMainMenu.prev_state
                    elif selection == ST_QUIT:
                        self.state = self.gameMainMenu.prev_state
                    elif selection != ST_RIGHT:
                        self.state = selection
                elif self.state == ST_GAME_INSTR:
                    max_page = 5
                    self.gameInstrMainMenu = self.get_game_instr_menu(ST_GAME_MAIN, instr_page_number)
                    self.gameInstrMainMenu.bg_image = self.menuBgImage
                    selection = self.gameInstrMainMenu.get_action()
                    if (selection == ST_GAME_MAIN or
                            (selection == ST_RIGHT and instr_page_number == max_page) or
                            (selection == ST_LEFT and instr_page_number == 1)):
                        instr_page_number = 1
                        self.state = self.gameInstrMainMenu.prev_state
                    elif selection == ST_LEFT:
                        instr_page_number -= 1
                    elif selection == ST_RIGHT:
                        instr_page_number += 1
                    elif selection == ST_QUIT:
                        self.state = self.gameInstrMainMenu.prev_state
                    else:
                        instr_page_number = int(selection)
                elif self.state == ST_SEL_PLAYERS:
                    if self.selPlayersMenu is None:
                        self.selPlayersMenu = self.get_select_players_menu()
                        self.selPlayersMenu.bg_image = self.menuBgImage
                    selection = self.selPlayersMenu.get_action()
                    if selection == ST_LEFT:
                        self.state = self.selPlayersMenu.prev_state
                    elif selection == ST_QUIT:
                        self.state = self.selPlayersMenu.prev_state
                    elif selection != ST_RIGHT:
                        players = []
                        for i in range(1, int(selection)+1):
                            players.append(Darts.Player("Player {0}".format(i)))
                        self.current_game.players = players
                        # print self.current_game.players
                        self.state = self.selPlayersMenu.next_state
                elif self.state == ST_SEL_VARIATION:
                    if self.selVariationMenu is None:
                        self.selVariationMenu = self.get_select_variation_menu()
                    if self.selVariationMenu is not None:
                        self.selVariationMenu.bg_image = self.menuBgImage
                        selection = self.selVariationMenu.get_action()
                        if selection == ST_LEFT:
                            self.state = self.selVariationMenu.prev_state
                        elif selection == ST_QUIT:
                            self.state = self.selVariationMenu.prev_state
                        elif selection != ST_RIGHT:
                            prev_state = self.state
                            self.current_game.variation = selection
                            self.state = self.selVariationMenu.next_state
                    else:
                        self.state = ST_SEL_SETTINGS
                elif self.state == ST_SEL_SETTINGS:
                    if self.selSettingsMenu is None:
                        self.selSettingsMenu = self.get_select_settings_menu()
                    if self.selSettingsMenu is not None:
                        self.selSettingsMenu.bg_image = self.menuBgImage
                        selection = self.selSettingsMenu.get_action()
                        if selection == ST_LEFT:
                            self.state = self.selSettingsMenu.prev_state
                        elif selection == ST_QUIT:
                            self.state = self.selSettingsMenu.prev_state
                        elif selection != ST_RIGHT:
                            self.current_game.set_setting(selection)  # TODO: implement this in Darts game
                            self.state = self.selSettingsMenu.next_state
                    else:
                        self.state = ST_SHOW_SUMMARY
                elif self.state == ST_SHOW_SUMMARY:
                    self.summaryMenu = self.get_summary_menu()
                    self.summaryMenu.bg_image = self.menuBgImage
                    selection = self.summaryMenu.get_action()
                    if selection == ST_LEFT:
                        self.state = self.summaryMenu.prev_state
                    elif selection == ST_QUIT:
                        self.state = self.summaryMenu.prev_state
                    else:
                        self.state =  self.summaryMenu.next_state
                elif self.state == ST_PLAY_GAME:
                    self.logger.log("Debug", "Play Game!")
                    self.state = ST_MAIN  # TODO: temporary...play game
                else:
                    self.logger.log("Error", "Unknown Menu State: " + self.state)
                    self.state = ST_MAIN  # TODO: ?

            self.logger.log("Debug", "Exiting run()")
        except Exception, e:
            print e
        finally:
            self.logger.stop()

    def show_intro(self):
        self.logger.log("Debug", "Entering show_intro()")
        intro = nammIntro.NammIntro(self.display_screen)
        intro.Run()
        intro = None
        self.logger.log("Debug", "Exiting show_intro()")

    def get_main_menu(self):
        self.logger.log("Debug", "Entering get_main_menu()")
        menu_items = ((menu.MENU_ITEM_RENDER_BLANK, None, None),
                      (menu.MENU_ITEM_RENDER_NORMAL, 'Replay Intro', ST_INTRO),
                      (menu.MENU_ITEM_RENDER_NORMAL, 'Games', ST_GAMES),
                      (menu.MENU_ITEM_RENDER_BLANK, None, None),
                      (menu.MENU_ITEM_RENDER_NORMAL, 'Quit', ST_QUIT))
        header = "Main Menu"
        font_size = 72  # int(math.ceil(self.display_screen.get_rect().height / (len(menu_items) + 3)))
        main_menu = menu.GameMenu(self.display_screen, menu_items, header, (0, 0, 0), self.menuFont, font_size)

        return main_menu

    def get_games_menu(self):
        self.logger.log("Debug", "Entering get_games_menu()")
        menu_items = [(menu.MENU_ITEM_RENDER_BLANK, None, None)]
        for game in get_game_list():
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, game, game))
        header = "Games"
        font_size = 72  # int(math.ceil(self.display_screen.get_rect().height / (len(menu_items) + 3)))
        games_menu = menu.GameMenu(self.display_screen, menu_items, header, (0, 0, 0), self.menuFont, font_size,
                                   nav_back=ST_LEFT, prev_state=ST_MAIN, next_state=ST_GAME_MAIN)

        return games_menu

    def get_select_variation_menu(self):
        self.logger.log("Debug", "Entering get_select_variation_menu()")
        # if self.current_game._variationOptions is None or len(self.current_game._variationOptions) == 0:
            # sel_variation_menu = None
        # else:
        if self.current_game._settingOptions is None or len(self.current_game._settingOptions) == 0:
            next_guy = ST_SHOW_SUMMARY
        else:
            next_guy = ST_SEL_SETTINGS

        menu_items = [(menu.MENU_ITEM_RENDER_BLANK, None, None)]
        for line in self.current_game._variationOptions:  # TODO: make variation options property
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, line, line))
        header = "Select Game Variation"
        font_size = 64  # int(math.ceil(self.display_screen.get_rect().height / (len(menu_items) + 3)))
        sel_variation_menu = menu.GameMenu(self.display_screen, menu_items, header, (0, 0, 0), self.menuFont,
                                           font_size, nav_back=ST_LEFT, prev_state=ST_SEL_PLAYERS,
                                           next_state=next_guy)

        return sel_variation_menu

    def get_select_settings_menu(self):
        self.logger.log("Debug", "Entering get_select_settings_menu()")
        # if self.current_game._settingOptions is None or len(self.current_game._settingOptions) == 0:
            # sel_settings_menu = None
        # else:
        if self.current_game._variationOptions is None or len(self.current_game._variationOptions) == 0:
            prev_guy = ST_SEL_PLAYERS
        else:
            prev_guy = ST_SEL_VARIATION

        menu_items = [(menu.MENU_ITEM_RENDER_BLANK, None, None)]
        for line in self.current_game._settingOptions:  # TODO: make settings options property
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, line, line))
        header = "Game Settings"
        font_size = 64  # int(math.ceil(self.display_screen.get_rect().height / (len(menu_items) + 3)))
        sel_settings_menu = menu.GameMenu(self.display_screen, menu_items, header, (0, 0, 0), self.menuFont,
                                           font_size, nav_back=ST_LEFT, prev_state=prev_guy,
                                           next_state=ST_SHOW_SUMMARY)

        return sel_settings_menu

    def get_select_players_menu(self):
        self.logger.log("Debug", "Entering get_select_players_menu()")

        if self.current_game._variationOptions is not None and len(self.current_game._variationOptions) > 0:
            next_guy = ST_SEL_VARIATION
        elif self.current_game._settingOptions is not None and len(self.current_game._settingOptions) > 0:
            next_guy = ST_SEL_SETTINGS
        else:
            next_guy = ST_SHOW_SUMMARY

        menu_items = [(menu.MENU_ITEM_RENDER_BLANK, None, None)]
        for option in self.current_game._playerOptions:  # TODO: make player options property
            if option == 1:
                line = str(option) + ' Player'
            else:
                line = str(option) + ' Players'
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, line, str(option)))
        header = "Select Number of Players"
        font_size = 48  # int(math.ceil(self.display_screen.get_rect().height / (len(menu_items) + 3)))
        sel_players_menu = menu.GameMenu(self.display_screen, menu_items, header, (0, 0, 0), self.menuFont,
                                         font_size, nav_back=ST_LEFT, prev_state=ST_GAME_MAIN,
                                         next_state=next_guy)

        return sel_players_menu

    def get_game_main_menu(self, prev_state):
        self.logger.log("Debug", "Entering get_game_main_menu()")

        menu_items = ((menu.MENU_ITEM_RENDER_BLANK, None, None),
                      (menu.MENU_ITEM_RENDER_NORMAL, 'Instructions', ST_GAME_INSTR),
                      (menu.MENU_ITEM_RENDER_NORMAL, 'High Scores', ST_GAME_MAIN),
                      (menu.MENU_ITEM_RENDER_NORMAL, 'Play', ST_SEL_PLAYERS),
                      )
        header = self.current_game.name
        font_size = 72  # int(math.ceil(self.display_screen.get_rect().height / (len(menu_items) + 3)))
        game_main_menu = menu.GameMenu(self.display_screen, menu_items, header, (0, 0, 0), self.menuFont,
                                       font_size, nav_back=ST_GAMES, prev_state=ST_GAMES,
                                       next_state=ST_SEL_PLAYERS)

        return game_main_menu

    def get_summary_menu(self):
        self.logger.log("Debug", "Entering get_summary_menu()")
        prev_guy = ST_SEL_PLAYERS

        menu_items = [(menu.MENU_ITEM_RENDER_BLANK, None, None)]
        menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, self.current_game.name, None))

        if self.current_game.variation is not None:
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, self.current_game.variation, None))
            if self.current_game.settings is None:
                prev_guy = ST_SEL_VARIATION

        if self.current_game.num_players == 1:
            num_players_text = str(self.current_game.num_players) + " Player"
        else:
            num_players_text = str(self.current_game.num_players) + " Players"
        menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, num_players_text, None))

       #  if self.current_game.settings is not None:
            # prev_guy = ST_SEL_SETTINGS
            # TODO: make games settings a dictionary and iterate here?
            # menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, self.current_game.settings, None))
        header = "Game Selection Summary"
        font_size = 64  # int(math.ceil(self.display_screen.get_rect().height / (len(menu_items) + 3)))
        summary_menu = menu.GameMenu(self.display_screen, menu_items, header, (0, 0, 0), self.menuFont,
                                           font_size, nav_back=ST_LEFT, nav_next=ST_RIGHT,
                                           prev_state=prev_guy, next_state=ST_PLAY_GAME)

        return summary_menu

    def get_game_instr_menu(self, prev_state, page_number):
        self.logger.log("Debug", "Entering get_game_instr_menu()")
        max_width = self.display_screen.get_rect().width - 20
        menu_items = []
        nav_back = None
        nav_next = None

        if page_number == 1:
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Summary:', None))
            menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))
    
            for line in self.current_game.instructions[Darts.INSTR_SUMMARY]:
                menu_items.append((menu.MENU_ITEM_RENDER_WRAP, line, None, max_width))

            nav_next = '2'

        elif page_number == 2:
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Object:', None))
            menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))

            for line in self.current_game.instructions[Darts.INSTR_OBJECT]:
                menu_items.append((menu.MENU_ITEM_RENDER_WRAP, line, None, max_width))

            nav_back = '1'
            nav_next = '3'

        elif page_number == 3:
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Game Play:', None))
            menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))

            for line in self.current_game.instructions[Darts.INSTR_GAMEPLAY]:
                menu_items.append((menu.MENU_ITEM_RENDER_WRAP, line, None, max_width))

            nav_back = '2'
            nav_next = '4'

        elif page_number == 4:
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Scoring:', None))
            menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))

            for line in self.current_game.instructions[Darts.INSTR_SCORING]:
                menu_items.append((menu.MENU_ITEM_RENDER_WRAP, line, None, max_width))

            nav_back = '3'
            nav_next = '5'

        elif page_number == 5:
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Variations:', None))
            menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))

            for line in self.current_game.instructions[Darts.INSTR_VARIATIONS]:
                menu_items.append((menu.MENU_ITEM_RENDER_WRAP, line, None, max_width))

            nav_back = '4'

        header = self.current_game.name
        font_size = 36  # int(math.ceil(self.display_screen.get_rect().height / (len(menu_items) + 3)))
        game_instr_menu = menu.GameMenu(self.display_screen, menu_items, header, (0, 0, 0), self.menuFont, font_size,
                                        nav_back=nav_back, nav_done=ST_GAME_MAIN, nav_next=nav_next,
                                        prev_state=ST_GAME_MAIN)

        return game_instr_menu
