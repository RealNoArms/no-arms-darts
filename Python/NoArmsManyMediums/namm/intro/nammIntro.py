"""

No Arms Many Mediums Intro Animation

    Copyright (C) 2013  Tim Kracht <timkracht4@gmail.com>

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

    Sprites and sound samples were borrowed from Chris Leathley's project,
    Jumpman - Under Construction: 

	http://members.iinet.net.au/~cleathley/jumpman/

"""


import pygame, sys, os
from pygame.locals import *
from namm.common.utilities import *

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
screen = pygame.display.set_mode((640,480))

import nammIntroSprites

class NammIntro:
    def __init__(self):
        self.RED = (128, 64, 64)
        self.CYAN = (110, 183, 193)
        self.PURPLE = (127, 59, 166)
        self.GREEN = (104, 169, 65)
        self.BLUE = (62, 49, 162)
        self.YELLOW = (203, 215, 101)
        self.ORANGE = (133, 83, 28)
        self.WHITE = (255, 255, 255)

        self.colorCycle = [self.RED, self.CYAN, self.PURPLE, self.GREEN, self.BLUE, self.YELLOW, self.ORANGE, self.WHITE]
        self.colorCycleIndex = 0
        self.noArmsColorCycles = 128

        self.backfill = pygame.Surface(screen.get_size())
        self.backfill.fill((0,0,0))
        self.backfillRect = self.backfill.get_rect()

        self.background = pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'jumpman_noarms.png'))
        self.background = self.background.convert()
        self.backgroundRect = self.background.get_rect()

        pygame.display.set_caption('...')

        self.jumpmanGroup = pygame.sprite.Group()
        self.lettersGroup = pygame.sprite.Group()
        self.laddersGroup = pygame.sprite.Group()

        nammIntroSprites.LadderTop.groups = self.laddersGroup
        nammIntroSprites.Jumpman.groups = self.jumpmanGroup
        nammIntroSprites.Letter.groups = self.lettersGroup
        nammIntroSprites.TitleText.groups = self.lettersGroup

        self.jumpman = nammIntroSprites.Jumpman((320,127), 'Standing')

        """ Dictionary of Tuple (Sprite, Destination X, Destination Y) keyed by letter """
        self.letters = { 'n': (nammIntroSprites.Letter((640, 127), 'n.png', self.colorCycle[self.colorCycleIndex]), 99, 246) }
        self.colorCycleIndex = wrap_increment(self.colorCycleIndex, len(self.colorCycle))
        self.letters['o'] = (nammIntroSprites.Letter((640, 127), 'o.png', self.colorCycle[self.colorCycleIndex]), 180, 246)
        self.colorCycleIndex = wrap_increment(self.colorCycleIndex, len(self.colorCycle))
        self.letters['a'] = (nammIntroSprites.Letter((640, 127), 'a.png', self.colorCycle[self.colorCycleIndex]), 277, 246)
        self.colorCycleIndex = wrap_increment(self.colorCycleIndex, len(self.colorCycle))
        self.letters['r'] = (nammIntroSprites.Letter((640, 127), 'r.png', self.colorCycle[self.colorCycleIndex]), 358, 246)
        self.colorCycleIndex = wrap_increment(self.colorCycleIndex, len(self.colorCycle))
        self.letters['m'] = (nammIntroSprites.Letter((640, 127), 'm.png', self.colorCycle[self.colorCycleIndex]), 447, 246)
        self.colorCycleIndex = wrap_increment(self.colorCycleIndex, len(self.colorCycle))
        self.letters['s'] = (nammIntroSprites.Letter((640, 127), 's.png', self.colorCycle[self.colorCycleIndex]), 531, 246)
        self.colorCycleIndex = wrap_increment(self.colorCycleIndex, len(self.colorCycle))

        self.leftLadderTop1 = nammIntroSprites.LadderTop((36, 141))
        self.leftLadderTop2 = nammIntroSprites.LadderTop((60, 141))
        self.rightLadderTop1 = nammIntroSprites.LadderTop((578, 141))
        self.leftLadderTop2 = nammIntroSprites.LadderTop((602, 141))

        self.fullCaption = 'No Arms Many Mediums Presents...'
        self.startVid = 0
        self.fadeInAlpha = 1
        self.introStep = 0
        self.colorCycleIndex = 0
        self.gameSpeed = 16
        self.delay = 0

    def Run(self):

	""" Show Python Power Pics """
	pygame.display.set_caption('Press S to Start')
        self.openingObjectsGroup = pygame.sprite.Group()
	nammIntroSprites.OpeningObjects.groups = self.openingObjectsGroup
	self.pressS = nammIntroSprites.OpeningObjects((320, 150), 'StoStart.png', 0)
	self.pythonPower = nammIntroSprites.OpeningObjects((320, 285), 'python-powered-h-140x182.png', 0)
	self.pygamePower = nammIntroSprites.OpeningObjects((320, 385), 'pygame_logo.png', 1)

	self.openingObjectsGroup.clear(screen, self.backfill)
	self.openingObjectsGroup.update()
	self.openingObjectsGroup.draw(screen)

	pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_s:
                    self.startVid = 1
                        
                """
                elif event.type == MOUSEBUTTONDOWN:
                    if introStep == 3:
                        jumpman.move_to_x(pygame.mouse.get_pos()[0], 16)
                """
            
            if self.introStep == 0 and self.startVid:
                # Pause Before Fading In
		pygame.display.set_caption('...')
                pygame.time.delay(2000)
                self.introStep += 1

            elif self.introStep == 1:
                # Fade In Screen
                self.background.set_alpha(self.fadeInAlpha)
                screen.blit(self.backfill, self.backfillRect)
                self.fadeInAlpha += 1

                if self.fadeInAlpha > 255:
                    self.introStep += 1
                else:
                    pygame.time.delay(10)

                screen.blit(self.background, self.backgroundRect)
                
            elif self.introStep == 2:
                # Pause Before Jumpman Appears
                pygame.time.delay(1000)
                self.jumpman.set_state('Growing')
                self.delay = 100
                self.introStep += 1

            elif self.introStep >= 3:
                if self.introStep == 3:
                    # grow Jumpman and pause
                    if self.jumpman.state == 'Standing':
                        # Standing means he's done growing
                        self.delay = 500
                        self.moved = 0
                        self.introStep += 1
                    
                elif self.introStep == 4:
                    # move jumpman to grab letters
                    if self.jumpman.state == 'Standing':
                        if self.moved:
                            # moved to letters, so start pulling them and go to next step
                            self.moved = 0
                            self.jumpman.move_to_x(47, self.gameSpeed)
                            self.introStep += 1
                        else:
                            # just starting, so move to the letters
                            self.moved = 1
                            self.jumpman.move_to_x(590, self.gameSpeed)
                            self.delay = 100
                    
                elif self.introStep == 5:
                    # move jumpman with letters to far left of screen
                    if self.jumpman.state == 'Standing':
                            # done moving letters to left, so start them moving to their chains and go to next step
                            self.letters['n'][0].move_to_x(self.letters['n'][1], self.gameSpeed)
                            self.letters['o'][0].move_to_x(self.letters['o'][1], self.gameSpeed)
                            self.letters['a'][0].move_to_x(self.letters['a'][1], self.gameSpeed)
                            self.letters['r'][0].move_to_x(self.letters['r'][1], self.gameSpeed)
                            self.letters['m'][0].move_to_x(self.letters['m'][1], self.gameSpeed)
                            self.letters['s'][0].move_to_x(640, self.gameSpeed) # troublemaker
                            
                            self.introStep += 1
                    else:
                        # move letters with jumpman
                        for letter in self.letters.viewvalues():
                            letter[0].pos = (self.jumpman.pos[0] + 50, letter[0].pos[1])            
                    
                elif self.introStep == 6:
                    # move jumpman and letters to right, drop letters down chains
                    self.lettersDone = 0

                    for letter in self.letters.viewkeys():
                        # [0] = sprite, [1] = x, [2] = y
                        if letter != 's' and self.letters[letter][0].state == 'Still':
                            if self.letters[letter][0].pos[0] == self.letters[letter][1] and self.letters[letter][0].pos[1] == self.letters[letter][2]:
                                # letter in final spot
                                self.lettersDone += 1
                                if letter == 'm':
                                    # if the m is secure, stop the falling sound
                                    self.letters[letter][0].fall.stop()
                            else:
                                # letter stopped over chain, so drop it
                                self.letters[letter][0].move_to_y(self.letters[letter][2], self.gameSpeed)
                                if letter == 'o':
                                    # start jumpman running back to center when o reaches its chain
                                    self.jumpman.move_to_x(320, self.gameSpeed)
                        elif letter == 's' and self.letters[letter][0].state == 'Still':
                                # s in final spot
                                self.lettersDone += 1
                    
                        pygame.display.set_caption(self.fullCaption[0:self.lettersDone] + '...')
                        
                    if self.lettersDone == len(self.letters) and self.jumpman.state == 'Standing':
                        # jumpman and all letters done moving
                        self.frustrationCount = 0
                        self.introStep += 1          
                                
                elif self.introStep == 7:
                    # jump in frustration at the s not dropping
                    self.frustrationCount += 1
                    self.jumpman.set_state('JumpingUp')
                    self.introStep += 1
                              
                elif self.introStep == 8:
                    # go grab the s again, after done jumping
                    if self.jumpman.state == 'Standing':
                        if self.jumpman.previousState == 'JumpingUp':
                            self.jumpman.move_to_x(590, self.gameSpeed)
                        else:
                            if self.frustrationCount == 1:
                                # grab s and move back to 'm' chain before releasing it
                                self.jumpman.move_to_x(self.letters['m'][1], self.gameSpeed)
                            else:
                                # grab s and move back to center
                                self.jumpman.move_to_x(320, self.gameSpeed)
                            self.introStep += 1
                                
                elif self.introStep == 9:
                    # drag S back to left
                    if self.jumpman.state == 'Standing':
                            # done moving s to left, release it
                            if self.frustrationCount == 1:
                                if self.letters['s'][0].pos[0] < 640:
                                    # first time, s goes back to far right, jumpman waits
                                    self.letters['s'][0].move_to_x(640, self.gameSpeed) # troublemaker
                                else:
                                    self.introStep = 7
                            elif self.frustrationCount == 2:
                                # second time, s continues further left while jumpman heads back far right
                                self.letters['s'][0].move_to_x(180, self.gameSpeed) # troublemaker
                                self.introStep += 1
                                
                    else:
                        # move letter s with jumpman
                        self.letters['s'][0].pos = (self.jumpman.pos[0] + 50, self.letters['s'][0].pos[1])
                                
                elif self.introStep == 10:
                    # jumpman runs ahead of s
                    if self.letters['s'][0].state == 'Still':
                        # s got to the far left, send it back to it's chain, and make jumpman run away from it
                        self.jumpman.move_to_x(608, self.gameSpeed)
                        self.letters['s'][0].move_to_x(self.letters['s'][1], self.gameSpeed)
                        self.introStep += 1
                                
                elif self.introStep == 11:
                    if self.jumpman.state == 'RunningLeft' and self.jumpman.pos[1] <= 575 and self.jumpman.previousState == 'Standing':
                        self.jumpman.set_state('JumpingLeft')
                    if self.letters['s'][0].state == 'Still':
                        # s gets to chain, drop it
                        if self.letters['s'][0].pos[0] == self.letters['s'][1] and self.letters['s'][0].pos[1] == self.letters['s'][2]:
                            # if s is secure, stop the falling sound
                            self.letters['s'][0].fall.stop()
                            if self.jumpman.state == 'Standing':
                                # s and jumpman in final spots, set his arms down
                                self.jumpman.set_state('DroppingArms')
                                
                                pygame.display.set_caption(self.fullCaption[0:7] + '...')
                                self.introStep += 1
                        else:
                            # s at chain, drop it
                            self.letters['s'][0].move_to_y(self.letters['s'][2], self.gameSpeed)
                            
                    elif self.jumpman.state == 'Standing' and self.letters['s'][0].pos[0] >= self.letters['m'][1] + 50:
                        # s over m's chain, so make Jumpman start running toward it to jump it
                        self.jumpman.move_to_x(320, self.gameSpeed)

                elif self.introStep == 12:
                    if self.jumpman.state == 'NoArms':
                        # Arms set down, show other title text
                        self.manyMediums = nammIntroSprites.TitleText((320, 285), 'manyMediums.png')
                        self.presents = nammIntroSprites.TitleText((320, 317), 'presents.png')
                        self.inspiration = nammIntroSprites.TitleText((320, 387), 'inspiration.png')

                        pygame.display.set_caption(self.fullCaption)

                        self.noArmsColorCycleCount = 0
                        self.colorCycleStartingIndex = 0
                        self.delay = 100
                        self.introStep += 1

                elif self.introStep == 13:
                    if self.noArmsColorCycleCount <= self.noArmsColorCycles:
                        self.noArmsColorCycleCount += 1
                        self.colorCycleStartingIndex = wrap_increment(self.colorCycleStartingIndex, len(self.colorCycle))
                        self.colorCycleIndex = self.colorCycleStartingIndex
                        self.letters['n'][0].color = self.colorCycle[self.colorCycleIndex]
                        self.colorCycleIndex = wrap_increment(self.colorCycleIndex, len(self.colorCycle))
                        self.letters['o'][0].color = self.colorCycle[self.colorCycleIndex]
                        self.colorCycleIndex = wrap_increment(self.colorCycleIndex, len(self.colorCycle))
                        self.letters['a'][0].color = self.colorCycle[self.colorCycleIndex]
                        self.colorCycleIndex = wrap_increment(self.colorCycleIndex, len(self.colorCycle))
                        self.letters['r'][0].color = self.colorCycle[self.colorCycleIndex]
                        self.colorCycleIndex = wrap_increment(self.colorCycleIndex, len(self.colorCycle))
                        self.letters['m'][0].color = self.colorCycle[self.colorCycleIndex]
                        self.colorCycleIndex = wrap_increment(self.colorCycleIndex, len(self.colorCycle))
                        self.letters['s'][0].color = self.colorCycle[self.colorCycleIndex]
                    else:
                        self.delay = 1000
                        self.nextLetter = 'n'
                        self.introStep += 1

                elif self.introStep == 14:
                    if self.nextLetter == 'n':
                        self.letters['n'][0].color = (0,0,0)
                        self.nextLetter = 'o'
                    elif self.nextLetter == 'o':
                        self.letters['o'][0].color = (0,0,0)
                        self.nextLetter = 'a'
                    elif self.nextLetter == 'a':
                        self.letters['a'][0].color = (0,0,0)
                        self.nextLetter = 'r'
                    elif self.nextLetter == 'r':
                        self.letters['r'][0].color = (0,0,0)
                        self.nextLetter = 'm'
                    elif self.nextLetter == 'm':
                        self.letters['m'][0].color = (0,0,0)
                        self.nextLetter = 's'
                    elif self.nextLetter == 's':
                        self.letters['s'][0].color = (0,0,0)
                        self.nextLetter = 'x'
                    else:
                        self.delay = 1000
                        self.introStep += 1
                    
                elif self.introStep == 15:
                    pygame.quit()
                    sys.exit()
                        
                        
                self.lettersGroup.clear(screen, self.background)
                self.jumpmanGroup.clear(screen, self.background)
                self.laddersGroup.clear(screen, self.background)
                
                self.lettersGroup.update()
                self.jumpmanGroup.update()
                self.laddersGroup.update()
                
                self.lettersGroup.draw(screen)
                self.jumpmanGroup.draw(screen)        
                self.laddersGroup.draw(screen)
                
            pygame.display.flip()
            pygame.time.delay(self.delay)

