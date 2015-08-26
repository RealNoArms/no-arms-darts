"""

Darts Menu

    Copyright (C) 2014-2015  Tim Kracht <timkracht4@gmail.com>

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

from namm.common.logger import Logger
from namm.common import menu
from namm.darts import darts

DARTS_GAME_MAIN = "Game Main Menu"
DARTS_INSTRUCTIONS = "Instructions"
DARTS_VARIATIONS = "Variations"
DARTS_SETTINGS = "Settings"
DARTS_PLAYERS = "Players"
DARTS_SELECTIONS = "Selections"


class DartMenu(menu.Menu):
    def __init__(self, game, screen, background, font, log_level="Warn"):
        super(DartMenu, self).__init__(None, False)
        if not os.path.exists("log"):
            os.mkdir("log")
        self._logger = Logger(log_level, os.path.join("log", "DartMenu.log"))
        self._logger.start()

        self._logger.log("Info", "Started Logging.")

        self._game = game
        self._screen = screen
        self._background = background
        self._font = font

        self._add_pages()

        self._state = DARTS_GAME_MAIN
        self._page = self._pages[self._state]
        self._page.background = self._background
        self._page.prev_state = menu.PAGE_ACTION_MAIN

    def get_action(self, no_action=None):
        menu_action = no_action
        page_action = None
        nav_next = None
        nav_prev = menu.PAGE_ACTION_MAIN
        self._page = self._pages[DARTS_GAME_MAIN]

        while menu_action is None:
            if page_action is None:
                page_action = self._page.get_action()

            if page_action == menu.PAGE_ACTION_QUIT or page_action == menu.PAGE_ACTION_GO:
                self._state = menu.PAGE_ACTION_MAIN
            elif page_action == menu.PAGE_ACTION_BACK:
                if nav_prev is not None:
                    self._state = nav_prev
            elif page_action == menu.PAGE_ACTION_NEXT or page_action == menu.PAGE_ACTION_DONE:
                if nav_next is not None:
                    self._state = nav_next
            elif page_action in (DARTS_GAME_MAIN, DARTS_INSTRUCTIONS, DARTS_VARIATIONS, DARTS_SETTINGS, DARTS_PLAYERS,
                                 DARTS_SELECTIONS, menu.PAGE_ACTION_MAIN, darts.INSTR_SUMMARY,
                                 darts.INSTR_OBJECT, darts.INSTR_GAMEPLAY, darts.INSTR_SCORING, darts.INSTR_VARIATIONS):
                self._state = page_action

            if self._state == DARTS_GAME_MAIN:
                page_action = None
                nav_next = None
                nav_prev = menu.PAGE_ACTION_MAIN
                self._page = self._pages[DARTS_GAME_MAIN]
            elif self._state == menu.PAGE_ACTION_MAIN:
                menu_action = page_action
            elif self._state == DARTS_INSTRUCTIONS or self._state == darts.INSTR_SUMMARY:
                page_action = None
                nav_next = darts.INSTR_OBJECT
                nav_prev = DARTS_GAME_MAIN
                self._page = self._pages[darts.INSTR_SUMMARY]
            elif self._state == darts.INSTR_OBJECT:
                page_action = None
                nav_next = darts.INSTR_GAMEPLAY
                nav_prev = darts.INSTR_SUMMARY
                self._page = self._pages[darts.INSTR_OBJECT]
            elif self._state == darts.INSTR_GAMEPLAY:
                page_action = None
                nav_next = darts.INSTR_SCORING
                nav_prev = darts.INSTR_OBJECT
                self._page = self._pages[darts.INSTR_GAMEPLAY]
            elif self._state == darts.INSTR_SCORING:
                page_action = None
                nav_next = darts.INSTR_VARIATIONS
                nav_prev = darts.INSTR_GAMEPLAY
                self._page = self._pages[darts.INSTR_SCORING]
            elif self._state == darts.INSTR_VARIATIONS:
                page_action = None
                nav_next = DARTS_GAME_MAIN
                nav_prev = darts.INSTR_SCORING
                self._page = self._pages[darts.INSTR_VARIATIONS]
            elif self._state == DARTS_VARIATIONS:
                if page_action == DARTS_VARIATIONS:
                    page_action = None
                    nav_next = None
                    nav_prev = DARTS_SELECTIONS
                    self._page = self._pages[DARTS_VARIATIONS]
                else:
                    self._game.variation = page_action
                    page_action = menu.PAGE_ACTION_BACK
            elif self._state == DARTS_SETTINGS:
                if page_action == DARTS_SETTINGS:
                    page_action = None
                    nav_next = None
                    nav_prev = DARTS_SELECTIONS
                    self._page = self._pages[DARTS_SETTINGS]
                else:
                    self._game.settings = page_action
                    page_action = menu.PAGE_ACTION_BACK
            elif self._state == DARTS_PLAYERS:
                if page_action == DARTS_PLAYERS:
                    page_action = None
                    nav_next = None
                    nav_prev = DARTS_SELECTIONS
                    self._page = self._pages[DARTS_PLAYERS]
                else:
                    print page_action
                    print int(page_action)
                    players = []
                    for i in range(1, int(page_action)+1):
                        players.append(darts.Player("Player {0}".format(i)))
                    self._game.players = players
                    page_action = menu.PAGE_ACTION_BACK
            elif self._state == DARTS_SELECTIONS:
                page_action = None
                nav_next = menu.PAGE_ACTION_MAIN
                nav_prev = DARTS_GAME_MAIN
                self._page = self._current_game_selections()

        return menu_action

    def _add_pages(self):
        self._logger.log("Debug", "Entering _add_pages()")

        max_width = self._screen.get_rect().width - 20
        self._pages = {}

        self._add_game_main_page(DARTS_GAME_MAIN)
        self._add_instr_summary_page(darts.INSTR_SUMMARY, max_width)
        self._add_instr_object_page(darts.INSTR_OBJECT, max_width)
        self._add_instr_gameplay_page(darts.INSTR_GAMEPLAY, max_width)
        self._add_instr_scoring_page(darts.INSTR_SCORING, max_width)
        self._add_instr_variations_page(darts.INSTR_VARIATIONS, max_width)
        self._add_variations_page(DARTS_VARIATIONS)
        self._add_players_page(DARTS_PLAYERS)
        self._add_settings_page(DARTS_SETTINGS)

    def _add_game_main_page(self, id):
        self._logger.log("Debug", "Entering _add_game_main_page()")
        menu_items = ((menu.MENU_ITEM_RENDER_BLANK, None, None),
                      (menu.MENU_ITEM_RENDER_NORMAL, DARTS_INSTRUCTIONS, DARTS_INSTRUCTIONS),
                      (menu.MENU_ITEM_RENDER_NORMAL, "Play", DARTS_SELECTIONS)
                      )
        # font_size = 72  int(math.ceil(self.display_screen.get_rect().height / (len(menu_items) + 3)))
        self._pages[id] = menu.MenuPage(id, self._screen, menu_items, self._game.name, (0, 0, 0), self._background,
                                        self._font, 72, nav_back=menu.PAGE_ACTION_BACK)

    def _add_instr_summary_page(self, id, max_width):
        self._logger.log("Debug", "Entering _add_instr_summary_page()")
        menu_items = []
        menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Summary:', None))
        menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))
        for line in self._game.instructions[darts.INSTR_SUMMARY]:
                menu_items.append((menu.MENU_ITEM_RENDER_WRAP, line, None, max_width))
        self._pages[id] = menu.MenuPage(id, self._screen, menu_items, self._game.name, (0, 0, 0),  self._background,
                                        self._font, 36, nav_back=menu.PAGE_ACTION_BACK, nav_next=menu.PAGE_ACTION_NEXT)

    def _add_instr_object_page(self, id, max_width):
        self._logger.log("Debug", "Entering _add_instr_object_page()")
        menu_items = []
        menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Object:', None))
        menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))
        for line in self._game.instructions[darts.INSTR_OBJECT]:
            menu_items.append((menu.MENU_ITEM_RENDER_WRAP, line, None, max_width))
        self._pages[id] = menu.MenuPage(id, self._screen, menu_items, self._game.name, (0, 0, 0),  self._background,
                                        self._font, 36, nav_back=menu.PAGE_ACTION_BACK, nav_next=menu.PAGE_ACTION_NEXT,
                                        nav_main=DARTS_GAME_MAIN)

    def _add_instr_gameplay_page(self, id, max_width):
        self._logger.log("Debug", "Entering _add_instr_gameplay_page()")
        menu_items = []
        menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Game Play:', None))
        menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))
        for line in self._game.instructions[darts.INSTR_GAMEPLAY]:
            menu_items.append((menu.MENU_ITEM_RENDER_WRAP, line, None, max_width))
        self._pages[id] = menu.MenuPage(id, self._screen, menu_items, self._game.name, (0, 0, 0),  self._background,
                                        self._font, 36, nav_back=menu.PAGE_ACTION_BACK, nav_next=menu.PAGE_ACTION_NEXT,
                                        nav_main=DARTS_GAME_MAIN)

    def _add_instr_scoring_page(self, id, max_width):
        self._logger.log("Debug", "Entering _add_instr_scoring_page()")
        menu_items = []
        menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Scoring:', None))
        menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))
        for line in self._game.instructions[darts.INSTR_SCORING]:
            menu_items.append((menu.MENU_ITEM_RENDER_WRAP, line, None, max_width))
        self._pages[id] = menu.MenuPage(id, self._screen, menu_items, self._game.name, (0, 0, 0),  self._background,
                                        self._font, 36, nav_back=menu.PAGE_ACTION_BACK, nav_next=menu.PAGE_ACTION_NEXT,
                                        nav_main=DARTS_GAME_MAIN)

    def _add_instr_variations_page(self, id, max_width):
        self._logger.log("Debug", "Entering _add_instr_variations_page()")
        menu_items = []
        menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, 'Variations:', None))
        menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))
        for line in self._game.instructions[darts.INSTR_VARIATIONS]:
            menu_items.append((menu.MENU_ITEM_RENDER_WRAP, line, None, max_width))
        self._pages[id] = menu.MenuPage(id, self._screen, menu_items, self._game.name, (0, 0, 0),  self._background,
                                        self._font, 36, nav_back=menu.PAGE_ACTION_BACK, nav_done=menu.PAGE_ACTION_DONE)

    def _current_game_selections(self):
        self._logger.log("Debug", "Entering _current_game_selections()")

        menu_items = []
        menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))
        menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, self._game.name, None))

        if self._game.variation is not None:
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, self._game.variation, DARTS_VARIATIONS))

        if self._game.num_players == 1:
            num_players_text = "1 Player"
        else:
            num_players_text = str(self._game.num_players) + " Players"
        menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, num_players_text, DARTS_PLAYERS))

        if self._game.settings is not None:
            # TODO: make games settings a dictionary and iterate here?
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, self._game.settings, DARTS_SETTINGS))

        menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, "Go!", menu.PAGE_ACTION_GO))
        return menu.MenuPage(id, self._screen, menu_items, "Game Selection Summary", (0, 0, 0),  self._background,
                             self._font, 64, nav_back=menu.PAGE_ACTION_BACK)

    def _add_players_page(self, id):
        self._logger.log("Debug", "Entering _add_players_page()")

        menu_items = []
        menu_items.append((menu.MENU_ITEM_RENDER_BLANK, None, None))
        for option in self._game.player_options:
            if option == 1:
                line = '1 Player'
            else:
                line = str(option) + ' Players'
            menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, line, str(option)))
        self._pages[id] =  menu.MenuPage(id, self._screen, menu_items, "Select Number of Players", (0, 0, 0),
                                         self._background, self._font, 48, nav_back=menu.PAGE_ACTION_BACK)

    def _add_settings_page(self, id):
        self._logger.log("Debug", "Entering _add_settings_page()")

        if self._game.setting_options is not None and len(self._game.setting_options) > 0:
            menu_items = [(menu.MENU_ITEM_RENDER_BLANK, None, None)]
            for line in self._game.setting_options:
                menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, line, line))
            self._pages[id] = menu.MenuPage(id, self._screen, menu_items, "Select Game Settings", (0, 0, 0),
                                            self._background, self._font, 64, nav_back=menu.PAGE_ACTION_BACK)

    def _add_variations_page(self, id):
        self._logger.log("Debug", "Entering _add_variations_page()")

        if self._game.variation_options is not None and len(self._game.variation_options) > 0:
            menu_items = [(menu.MENU_ITEM_RENDER_BLANK, None, None)]
            for line in self._game.variation_options:
                menu_items.append((menu.MENU_ITEM_RENDER_NORMAL, line, line))
            self._pages[id] = menu.MenuPage(id, self._screen, menu_items, "Select Game Variation", (0, 0, 0),
                                            self._background, self._font, 64, nav_back=menu.PAGE_ACTION_BACK)