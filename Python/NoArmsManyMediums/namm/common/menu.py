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
import math
from pygame.locals import *
from itertools import chain

MENU_ITEM_RENDER_NORMAL = 0
MENU_ITEM_RENDER_HFIT = 1
MENU_ITEM_RENDER_WRAP = 2
MENU_ITEM_RENDER_BLANK = 3
MENU_ITEM_RENDER_TYPES = (MENU_ITEM_RENDER_NORMAL,
                          MENU_ITEM_RENDER_HFIT,
                          MENU_ITEM_RENDER_WRAP,
                          MENU_ITEM_RENDER_BLANK)


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


# The Main, Game Menu Class
# items = [renderType, text, action, max_width]
class GameMenu():
    def __init__(self, screen, items, header=None, bg_color=(0, 0, 0), font=None, font_size=30,
                 font_color=(255, 255, 255), nav_back=None, nav_done=None, nav_next=None, nav_main=None,
                 prev_state=None, next_state=None):
 
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        self.bg_color = bg_color
        self.bg_image = None
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color
        self.nav_back = nav_back
        self.nav_done = nav_done
        self.nav_next = nav_next
        self.nav_main = nav_main
        self.prev_state = prev_state
        self.next_state = next_state

        self.base_message_font_size = int(self.scr_height * .15)
        
        self.items = []
        menu_item = None
        nav_flag = False
        pos_y = 25    # arbitrary top for now

        if header is not None:
            header_font_size = int(1.5 * font_size)
            header_item = MenuItem(header, None, font, header_font_size)
            pos_x = (self.scr_width / 2) - (header_item.width / 2)
            header_item.set_position(pos_x, pos_y)
            self.items.append(header_item)
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
                    for line in wrapline(item_text, test_font, max_width):
                        menu_item = MenuItem(line, item_action, font, font_size)
                        pos_x = (self.scr_width / 2) - (menu_item.width / 2)
                        menu_item.set_position(pos_x, pos_y)
                        pos_y = pos_y + menu_item.height
                        self.items.append(menu_item)
                        menu_item = None
                else:
                    menu_item = MenuItem(item_text, item_action, font, font_size)
            else:
                menu_item = MenuItem(item_text, item_action, font, font_size)

            if menu_item is not None:
                pos_x = (self.scr_width / 2) - (menu_item.width / 2)
                menu_item.set_position(pos_x, pos_y)
                pos_y = pos_y + menu_item.height
                self.items.append(menu_item)

        # Navigation
        if self.nav_back is not None:
            menu_item = MenuItem("", None, font, font_size)
            pos_y = pos_y + menu_item.height + menu_item.height
            menu_item = MenuItem('Back', self.nav_back, font, font_size)
            pos_x = (self.scr_width / 3) - (menu_item.width / 2)
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)
            nav_flag = True

        if self.nav_done is not None:
            if not nav_flag:
                menu_item = MenuItem("", None, font, font_size)
                pos_y = pos_y + menu_item.height + menu_item.height
            menu_item = MenuItem('Done', self.nav_done, font, font_size)
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)
            nav_flag = True

        if self.nav_next is not None:
            if not nav_flag:
                menu_item = MenuItem("", None, font, font_size)
                pos_y = pos_y + menu_item.height + menu_item.height
            menu_item = MenuItem('Next', self.nav_next, font, font_size)
            pos_x = (2 * self.scr_width / 3) - (menu_item.width / 2)
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)
            nav_flag = True

        if self.nav_main is not None:
            if not nav_flag:
                menu_item = MenuItem("", None, font, font_size)
                self.items.append(menu_item)
                pos_y = pos_y + menu_item.height
            pos_y = pos_y + menu_item.height
            menu_item = MenuItem('Main', self.nav_main, font, font_size)
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)
        self.clock = pygame.time.Clock()
 
    def get_action(self):
        action = None

        while action is None:
            # Limit frame speed to 50 FPS
            self.clock.tick(50)

            # Redraw the background
            self.screen.fill(self.bg_color)
            if self.bg_image is not None:
                self.bg_image.set_alpha(64)
                self.screen.blit(self.bg_image, [0, 0])
                
            mpos = pygame.mouse.get_pos()
            
            for item in self.items:
                if item.is_mouse_selection(mpos) and item.action is not None:
                    item.set_font_color((255, 255, 0))
                    item.set_italic(True)
                else:
                    item.set_font_color((255, 255, 255))
                    item.set_italic(False)
                self.screen.blit(item.label, item.position)

            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    action = 'Quit'
                    break
                elif event.type == KEYDOWN and event.key in (K_q, K_ESCAPE):
                    action = 'Quit'
                    break
                elif event.type == KEYDOWN and event.key == K_LEFT:
                    action = 'Left'
                    break
                elif event.type == KEYDOWN and event.key == K_RIGHT:
                    action = 'Right'
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self.items:
                        if item.is_mouse_selection(mpos):
                            action = item.action

        return action


def truncline(text, font, maxwidth):
        real = len(text)
        stext = text
        l = font.size(text)[0]
        cut = 0
        a = 0
        done = 1
        # old = None
        while l > maxwidth:
            a += 1
            n = text.rsplit(None, a)[0]
            if stext == n:
                cut += 1
                stext = n[:-cut]
            else:
                stext = n
            l = font.size(stext)[0]
            real = len(stext)
            done = 0
        return real, done, stext             


def wrapline(text, font, maxwidth): 
    done = 0
    wrapped = []
                               
    while not done:             
        nl, done, stext = truncline(text, font, maxwidth)
        wrapped.append(stext.strip())                  
        text = text[nl:]
    return wrapped
 
 
def wrap_multi_line(text, font, maxwidth):
    """ returns text taking new lines into account.
    """
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)
