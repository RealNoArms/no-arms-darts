"""

Menu

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

    Built on code from (Auto-)Didactic Programming:
        http://nebelprog.wordpress.com/

    And the pygame wiki:
        http://www.pygame.org/wiki/textwrapping
"""

import pygame
from pygame.locals import *

from error import Error
from utilities import wrap_line

MENU_ITEM_RENDER_NORMAL = 0
MENU_ITEM_RENDER_HFIT = 1
MENU_ITEM_RENDER_WRAP = 2
MENU_ITEM_RENDER_BLANK = 3
MENU_ITEM_RENDER_TYPES = (MENU_ITEM_RENDER_NORMAL,
                          MENU_ITEM_RENDER_HFIT,
                          MENU_ITEM_RENDER_WRAP,
                          MENU_ITEM_RENDER_BLANK)

PAGE_ACTION_BACK = "Back"
PAGE_ACTION_DONE = "Done"
PAGE_ACTION_MAIN = "Main"
PAGE_ACTION_NEXT = "Next"
PAGE_ACTION_QUIT = "Quit"
PAGE_ACTION_GO = "Go!"
PAGE_ACTION_NO_ACTION = "X"


# The basic Menu Item class
class MenuItem(pygame.font.Font):
    def __init__(self, text, action=None, font=None, font_size=30,
                 font_color=(255, 255, 255), (pos_x, pos_y)=(0, 0)):
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.action = action
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.get_label()
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = pos_x, pos_y

    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y

    def is_mouse_selection(self, (posx, posy)):
        if (self.pos_x <= posx <= self.pos_x + self.width) and (self.pos_y <= posy <= self.pos_y + self.height):
            return True
        return False

    def set_font_color(self, rgb_tuple):
        self.font_color = rgb_tuple
        self.label = self.get_label()

    def get_label(self):
        return self.render(self.text, 1, self.font_color)


# A menu page
# items = [renderType, text, action, max_width]
class MenuPage(object):
    def __init__(self, id, screen, items, header=None, bg_color=(0, 0, 0), bg_image=None, font=None, font_size=30,
                 font_color=(255, 255, 255), nav_back=None, nav_done=None, nav_next=None, nav_main=None):
        self._id = id
        self._screen = screen

        self._screen_width = self._screen.get_rect().width
        self._screen_height = self._screen.get_rect().height
        self._bg_color = bg_color
        self._bg_image = bg_image

        self._font = pygame.font.SysFont(font, font_size)
        self._font_color = font_color
        self._nav_back = nav_back
        self._nav_done = nav_done
        self._nav_next = nav_next
        self._nav_main = nav_main

        self._base_message_font_size = int(self._screen_height * .15)
        
        self._items = []
        menu_item = None
        nav_flag = False
        pos_y = 25    # arbitrary top for now

        if header is not None:
            header_font_size = int(1.5 * font_size)
            header_item = MenuItem(header, None, font, header_font_size)
            pos_x = (self._screen_width / 2) - (header_item.width / 2)
            header_item.set_position(pos_x, pos_y)
            self._items.append(header_item)
            pos_y = pos_y + header_item.height

        for index, item in enumerate(items):
            item_render = item[0]
            item_text = item[1]
            item_action = item[2]
            max_width = None
            if len(item) >= 4:
                max_width = item[3]
            
            if item_render == MENU_ITEM_RENDER_BLANK:
                menu_item = MenuItem("", None, font, font_size)
            elif item_render == MENU_ITEM_RENDER_HFIT:
                new_size = font_size
                test_font = pygame.font.Font(font, new_size)
                while (max_width is not None
                       and test_font.size(item_text)[0] > max_width
                       and new_size > 5):
                    if new_size <= 10:
                        new_size -= 1
                    elif new_size <= 30:
                        new_size -= 2
                    else:
                        new_size -= 5
                    test_font = pygame.font.Font(font, new_size)
                menu_item = MenuItem(item_text, item_action, font, new_size)
            elif item_render == MENU_ITEM_RENDER_WRAP:
                test_font = pygame.font.Font(font, font_size)
                if max_width is not None:
                    for line in wrap_line(item_text, test_font, max_width):
                        menu_item = MenuItem(line, item_action, font, font_size)
                        pos_x = (self._screen_width / 2) - (menu_item.width / 2)
                        menu_item.set_position(pos_x, pos_y)
                        pos_y = pos_y + menu_item.height
                        self._items.append(menu_item)
                        menu_item = None
                else:
                    menu_item = MenuItem(item_text, item_action, font, font_size)
            else:
                menu_item = MenuItem(item_text, item_action, font, font_size)

            if menu_item is not None:
                pos_x = (self._screen_width / 2) - (menu_item.width / 2)
                menu_item.set_position(pos_x, pos_y)
                pos_y = pos_y + menu_item.height
                self._items.append(menu_item)

        # Navigation
        if self._nav_back is not None:
            menu_item = MenuItem("", None, font, font_size)
            pos_y = pos_y + menu_item.height + menu_item.height
            menu_item = MenuItem('Back', self._nav_back, font, font_size)
            pos_x = (self._screen_width / 3) - (menu_item.width / 2)
            menu_item.set_position(pos_x, pos_y)
            self._items.append(menu_item)
            nav_flag = True

        if self._nav_done is not None:
            if not nav_flag:
                menu_item = MenuItem("", None, font, font_size)
                pos_y = pos_y + menu_item.height + menu_item.height
            menu_item = MenuItem('Done', self._nav_done, font, font_size)
            pos_x = (self._screen_width / 2) - (menu_item.width / 2)
            menu_item.set_position(pos_x, pos_y)
            self._items.append(menu_item)
            nav_flag = True

        if self._nav_next is not None:
            if not nav_flag:
                menu_item = MenuItem("", None, font, font_size)
                pos_y = pos_y + menu_item.height + menu_item.height
            menu_item = MenuItem('Next', self._nav_next, font, font_size)
            pos_x = (2 * self._screen_width / 3) - (menu_item.width / 2)
            menu_item.set_position(pos_x, pos_y)
            self._items.append(menu_item)
            nav_flag = True

        if self._nav_main is not None:
            if not nav_flag:
                menu_item = MenuItem("", None, font, font_size)
                self._items.append(menu_item)
                pos_y = pos_y + menu_item.height
            pos_y = pos_y + menu_item.height
            menu_item = MenuItem('Main', self._nav_main, font, font_size)
            pos_x = (self._screen_width / 2) - (menu_item.width / 2)
            menu_item.set_position(pos_x, pos_y)
            self._items.append(menu_item)
        self._clock = pygame.time.Clock()

    # Properties
    @property
    def id(self):
        return self._id

    @property
    def background(self):
        return self._bg_image

    @background.setter
    def background(self, value):
        self._bg_image = value

    # Methods
    def get_action(self, no_action=None):
        action = no_action

        # Display-only screen, show it and return the no action action
        if action == PAGE_ACTION_NO_ACTION:
            self._screen.fill(self._bg_color)
            if self._bg_image is not None:
                self._bg_image.set_alpha(64)
                self._screen.blit(self._bg_image, [0, 0])

            for item in self._items:
                item.set_font_color((255, 255, 255))
                self._screen.blit(item.label, item.position)

            pygame.display.flip()

        while action is None:
            # Limit frame speed to 50 FPS
            self._clock.tick(50)

            # Redraw the background
            self._screen.fill(self._bg_color)
            if self._bg_image is not None:
                self._bg_image.set_alpha(64)
                self._screen.blit(self._bg_image, [0, 0])
                
            mpos = pygame.mouse.get_pos()
            
            for item in self._items:
                if item.is_mouse_selection(mpos) and item.action is not None:
                    item.set_font_color((255, 255, 0))
                    item.set_italic(True)
                else:
                    item.set_font_color((255, 255, 255))
                    item.set_italic(False)
                self._screen.blit(item.label, item.position)

            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    action = PAGE_ACTION_QUIT
                    break
                elif event.type == KEYDOWN and event.key in (K_q, K_ESCAPE):
                    action = PAGE_ACTION_BACK
                    break
                elif event.type == KEYDOWN and event.key == K_LEFT:
                    action = PAGE_ACTION_BACK
                    break
                elif event.type == KEYDOWN and event.key == K_RIGHT:
                    action = PAGE_ACTION_NEXT
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self._items:
                        if item.is_mouse_selection(mpos):
                            action = item.action

        return action


class Menu(object):
    def __init__(self, pages=None, wrap=False):
        self._pages = pages
        self._page = None
        self._wrap = wrap

        # pagination
        if pages is not None:
            self._page_count = len(pages)
        else:
            self._page_count = 0

    # Properties
    def background(self, value):
        for key,val in self._pages.items():
            val.background = value

    @property
    def page_id(self):
        return self._page.id

    @page_id.setter
    def page_id(self, value):
        if value in self._pages:
            self._page = self._pages[value]
        else:
            raise InvalidMenuPageError("Invalid Page Id!", value)

    @property
    def wrap(self):
        return self._wrap

    @wrap.setter
    def wrap(self, value):
        self._wrap = value

    # Methods
    def add_page(self, page):
        if self._pages is None:
            self._pages = {page.id: page}
        else:
            self._pages[page.id] = page
        self._page_count = len(self._pages)

    def get_action(self, no_action=None):
        action = no_action

        if self._page is not None:
            action = self._page.get_action(action)
        # TODO: this here next and now
        return action


# Errors
class MenuError(Error):

    def __init__(self, msg=None, obj=None):
        super(MenuError, self).__init__(msg, obj)
        self._rep = "Menu Error"


class InvalidMenuPageError(MenuError):

    def __init__(self, msg=None, obj=None):
        super(InvalidMenuPageError, self).__init__(msg, obj)
        self._rep = "Invalid Menu Page Error"
