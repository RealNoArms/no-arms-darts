'''

Python-Arduino Serial test 2

Free To The People

Pygame Game Menu based on code from (Auto-)Didactic Programming
http://nebelprog.wordpress.com/

'''
import sys
import time
import serial
from struct import unpack
import pygame

pygame.init()

class MenuItem(pygame.font.Font):
    def __init__(self, text, font=None, font_size=30,
                 font_color=(255, 255, 255), (pos_x, pos_y)=(0, 0)):
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
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
        if (posx >= self.pos_x and posx <= self.pos_x + self.width) and (posy >= self.pos_y and posy <= self.pos_y + self.height):
            return True
        return False

    def set_font_color(self, rgb_tuple):
        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)
        
class GameMenu():
    def __init__(self, screen, items, bg_color=(0,0,0),font=None, font_size=30, font_color=(255, 255, 255)):
 
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        self.bg_color = bg_color
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color
        self.items = []
        for index, item in enumerate(items):
            menu_item = MenuItem(item)
 
            # t_h: total height of text block
            t_h = len(items) * menu_item.height
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            pos_y = (self.scr_height / 2) - (t_h / 2) + (index * menu_item.height)
 
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)
        self.clock = pygame.time.Clock()

    def display_status(self, status_text):
        status_item = MenuItem(status_text)
        pos_x = (self.scr_width / 2) - (status_item.width / 2)
        pos_y = (self.scr_height / 2) - (status_item.height / 2)
        status_item.set_position(pos_x, pos_y)
        status_item.set_font_color((255, 255, 255))
        status_item.set_italic(False)
        
        self.screen.fill(self.bg_color)
        self.screen.blit(status_item.label, status_item.position)
        
        pygame.display.flip()
 
    def run(self, ser):
        mainloop = True
        acceptInput = True
        returnvalue = 'Quit'

        while mainloop:
            while ser.inWaiting() > 0:
                if ser.read() == 'H':
                    s1 = ser.read()
                    s2 = ser.read()

                    wedge = unpack('b' * len(s1), s1)[0]
                    multiplier = unpack('b' * len(s2), s2)[0]
            
                    hitMessage = []
                    
                    if multiplier == 1:
                        hitMessage.append("Single ")
                    elif multiplier == 2:
                        hitMessage.append("Double ")
                    elif multiplier == 3:
                        hitMessage.append("Triple ")
                    else:
                        hitMessage.append("Unknown ")

                    if wedge == 25:
                        hitMessage.append("Bullseye")
                    else:
                        hitMessage.append("{0:d}".format(wedge))

                    self.display_status(''.join(hitMessage))

                    millis = 0
                    while millis < 3000 and ser.inWaiting() == 0:
                        pygame.time.wait(1)
                        millis = millis + 1
                    
            # Limit frame speed to 50 FPS
            self.clock.tick(50)
            mpos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self.items:
                        if item.is_mouse_selection(mpos):
                            mainloop = False
                            returnValue = item.text
 
            # Redraw the background
            self.screen.fill(self.bg_color)
            for item in self.items:
                if item.is_mouse_selection(mpos):
                    item.set_font_color((255, 0, 0))
                    item.set_italic(True)
                else:
                    item.set_font_color((255, 255, 255))
                    item.set_italic(False)
                self.screen.blit(item.label, item.position)
            pygame.display.flip()
        return returnValue
   
def connect_board(connected, ser, gm):
    requestCount = 1
    result = connected
    while not result and requestCount <= maxRequests:
        if requestCount >= maxRequests:
            gm.display_status("No response after {0:d} tries, giving up.".format(requestCount-1))
            pygame.time.wait(3000)
            
        gm.display_status("Sending connection request #{0:d} to dartboard...".format(requestCount))
        ser.write('C')
        requestCount += 1
        result = (ser.read() == 'C')
        if not result:
            gm.display_status('No response...')
            pygame.time.wait(3000)
        else:
            gm.display_status('Connected to dartboard!')
            pygame.time.wait(3000)
    return result
                   

def disconnect_board(connected, ser, gm):
    result = connected
    if connected:
        gm.display_status('Disconnecting dartboard...')
        
        ser.write('D')
        ser.read()
                    
        ser.write('Q')
        while (ser.read() != 'D'):
            ser.write('Q')

        gm.display_status('Dartboard disconnected!')
        pygame.time.wait(3000)
        result = False
    return result


def play_game(game_status, ser, gm):
    requestCount = 1
    result = game_status
    playing = (game_status == 'Playing')
    while not playing and requestCount <= maxRequests:
        if requestCount >= maxRequests:
            gm.display_status("No response after {0:d} tries, giving up.".format(requestCount-1))
            pygame.time.wait(3000)

        gm.display_status("Sending play request #{0:d} to dartboard...".format(requestCount))
        ser.write('P')
        requestCount += 1
        playing = (ser.read() == 'P')
        if not playing:
            gm.display_status('No response...')
            pygame.time.wait(3000)
        else:
            gm.display_status('Started a game!')
            pygame.time.wait(3000)
            result = 'Playing'
    return result


def stop_game(game_status, ser, gm):
    result = game_status
    if game_status != 'Stopped':
        gm.display_status('Stopping game...')
        ser.write('X')
        ser.read()
                
        ser.write('Q')
        while (ser.read() != 'X'):
            ser.write('Q')

        gm.display_status('Game stopped!')
        pygame.time.wait(3000)
        result = 'Stopped'
    return result

maxRequests = 5

ser = serial.Serial("COM3", 9600)
# *nix: ser = serial.Serial('/dev/ttyblah1', 9600)  or whetever
# TODO: look at scan example to try to automagically find the right port?

ser.timeout = 5

menu_items = ('Connect', 'Play', 'Stop', 'Disconnect', 'Quit')
screen = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.set_caption('Serial Test 2')
gm = GameMenu(screen, menu_items)
running = True
connected = False
game_status = 'Stopped'

while running:
    result = gm.run(ser)
    if result == 'Connect':
        connected = connect_board(connected, ser, gm)
    elif result == 'Play':
        if connected:
            game_status = play_game(game_status, ser, gm)
        else:
            gm.display_status('Not connected to the dartboard!')
            pygame.time.wait(3000)
    elif result == 'Stop':
        game_status = stop_game(game_status, ser, gm)
    elif result == 'Disconnect':
        game_status = stop_game(game_status, ser, gm)
        connected = disconnect_board(connected, ser, gm)
    else:
        if connected:
            game_status = stop_game(game_status, ser, gm)
            connected = disconnect_board(connected, ser, gm) 
        running = False

pygame.quit()
sys.exit()
