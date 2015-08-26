"""

Sprites for the No Arms Many Mediums Intro


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
"""

import pygame
import os
from pygame.locals import *
from namm.common.utilities import *


# the sprite state class
class SpriteState:
    def __init__(self, state_name):
        self.name = state_name
        self.images = None


# tops of ladders (so jumpman appears behind them)
class LadderTop(pygame.sprite.Sprite):

    image = pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'ladderTop.png'))
    image.convert()
    
    def __init__(self, init_pos):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = LadderTop.image
        self.pos = init_pos
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = self.pos
       
       
# the jumpman sprite
class Jumpman(pygame.sprite.Sprite):

    grow = pygame.mixer.Sound(os.path.join('namm', 'sounds', 'NoArmsIntro', 'JumpmanAppear.wav'))
    jump = pygame.mixer.Sound(os.path.join('namm', 'sounds', 'NoArmsIntro', 'Jump.wav'))
    footStep = pygame.mixer.Sound(os.path.join('namm', 'sounds', 'NoArmsIntro', 'FootStep.wav'))
    dropArm = pygame.mixer.Sound(os.path.join('namm', 'sounds', 'NoArmsIntro', 'SpearThrow.wav'))
    huh = pygame.mixer.Sound(os.path.join('namm', 'sounds', 'NoArmsIntro', 'Bounce.wav'))

    standingState = SpriteState('Standing')
    standingState.images = [pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'StandStill.png'))]
    standingState.images[0] = standingState.images[0].convert()
    standingState.images[0].set_colorkey(standingState.images[0].get_at((0, 0)), RLEACCEL)
    
    runningLeftState = SpriteState('RunningLeft')
    runningLeftState.images = [pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'RunLeft1.png')),
                               pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'RunLeft2.png'))]
    for i in range(len(runningLeftState.images)):
        runningLeftState.images[i] = runningLeftState.images[i].convert()
        runningLeftState.images[i].set_colorkey(runningLeftState.images[i].get_at((0, 0)), RLEACCEL)
    
    runningRightState = SpriteState('RunningRight')
    runningRightState.images = []
    for img in runningLeftState.images:
        runningRightState.images.append(pygame.transform.flip(img, 1, 0))

    jumpingUpState = SpriteState('JumpingUp')
    jumpingUpState.images = [pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'JumpCenter.png'))]
    jumpingUpState.images[0] = jumpingUpState.images[0].convert()
    jumpingUpState.images[0].set_colorkey(jumpingUpState.images[0].get_at((0, 4)), RLEACCEL)

    jumpingLeftState = SpriteState('JumpingLeft')
    jumpingLeftState.images = [pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'JumpLeft.png'))]
    jumpingLeftState.images[0] = jumpingLeftState.images[0].convert()
    jumpingLeftState.images[0].set_colorkey(jumpingLeftState.images[0].get_at((0, 0)), RLEACCEL)
    
    jumpingRightState = SpriteState('JumpingRight')
    jumpingRightState.images = []
    for img in jumpingLeftState.images:
        jumpingRightState.images.append(pygame.transform.flip(img, 1, 0))
    
    droppingArmsState = SpriteState('DroppingArms')
    droppingArmsState.images = [pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'DropArms1.png')),
                                pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'DropArms2.png')),
                                pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'DropArms3.png')),
                                pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'DropArms4.png')),
                                pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'DropArms5.png')),
                                pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'DropArms6.png')),
                                pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'DropArms7.png')),
                                pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'DropArms8.png'))]
    for i in range(len(droppingArmsState.images)):
        droppingArmsState.images[i] = droppingArmsState.images[i].convert()
        droppingArmsState.images[i].set_colorkey(droppingArmsState.images[i].get_at((0, 0)), RLEACCEL)
    
    growingState = SpriteState('Growing')
    growingState.images = [pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'Grow1.png')),
                           pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'Grow2.png')),
                           pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'Grow3.png')),
                           pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'Grow4.png')),
                           pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'Grow5.png')),
                           pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'Grow6.png')),
                           pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'Grow7.png')),
                           pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'Grow8.png')),
                           pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'Grow9.png'))]
    for i in range(len(growingState.images)):
        growingState.images[i] = growingState.images[i].convert()
        growingState.images[i].set_colorkey(growingState.images[i].get_at((0, 0)), RLEACCEL)
        
    noArmsState = SpriteState('NoArms')
    noArmsState.images = [pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', 'DropArms8.png'))]
    noArmsState.images[0] = noArmsState.images[0].convert()
    noArmsState.images[0].set_colorkey(noArmsState.images[0].get_at((0, 0)), RLEACCEL)

    states = {standingState.name: standingState, runningLeftState.name: runningLeftState,
              runningRightState.name: runningRightState, jumpingUpState.name: jumpingUpState,
              jumpingLeftState.name: jumpingLeftState, jumpingRightState.name: jumpingRightState,
              droppingArmsState.name: droppingArmsState, noArmsState.name: noArmsState,
              growingState.name: growingState}

    jumpHeight = 8
    jumpSpeed = 2
    
    def __init__(self, init_pos, init_state_name):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = init_pos
        self.state = init_state_name
        self.imageIndex = 0
        self.velocity = (0, 0)

        self.image = None
        self.rect = None
        self.previousState = None
        self.targetY = None
        self.targetX = None

    def update(self):
        self.image = Jumpman.states[self.state].images[self.imageIndex]
        self.imageIndex = wrap_increment(self.imageIndex, len(Jumpman.states[self.state].images))
        
        if self.state == 'DroppingArms':
            if self.imageIndex == 0:
                self.set_state('NoArms')
                Jumpman.huh.play()
            elif self.imageIndex in [4, 7]:
                Jumpman.dropArm.play()
        elif self.state == 'Growing' and self.imageIndex == 0:
            self.set_state('Standing')
            
        self.rect = self.image.get_rect()
        self.pos = (self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1])
        if ((self.state == 'RunningLeft' and self.pos[0] <= self.targetX) or
                (self.state == 'RunningRight' and self.pos[0] >= self.targetX)):
            self.pos = (self.targetX, self.pos[1])
            self.velocity = (0, 0)
            self.set_state('Standing')
        elif self.state in ['JumpingUp', 'JumpingLeft', 'JumpingRight']:
            if self.velocity[1] < 0 and self.pos[1] <= self.targetY:
                self.pos = (self.pos[0], self.targetY)
                self.velocity = (self.velocity[0], 0)
            elif self.velocity[1] == 0:
                self.velocity = (self.velocity[0], Jumpman.jumpSpeed)
                self.targetY = self.pos[1] + Jumpman.jumpHeight
            elif self.velocity[1] > 0 and self.pos[1] >= self.targetY:
                self.pos = (self.pos[0], self.targetY)
                self.velocity = (self.velocity[0], 0)
                # assumes jumpman does not attain move_to_x position before jump is complete if running left or right
                self.set_state(self.previousState)

        if self.state in ['RunningLeft', 'RunningRight']:
            Jumpman.footStep.play()
            
        self.rect.center = self.pos

    def set_state(self, new_state_name):
        self.previousState = self.state
        self.state = new_state_name
        self.imageIndex = 0
        if new_state_name in ['JumpingUp', 'JumpingLeft', 'JumpingRight']:
            self.targetY = self.pos[1] - Jumpman.jumpHeight 
            self.velocity = (self.velocity[0], -Jumpman.jumpSpeed)
            Jumpman.jump.play()
        elif new_state_name == 'DroppingArms':
            self.pos = (self.pos[0], self.pos[1] - 6)
        elif new_state_name == 'Growing':
            Jumpman.grow.play()

    def move_to_x(self, new_x, speed):
        if new_x != self.pos[0]:
            self.targetX = new_x
            if new_x > self.pos[0]:
                self.set_state('RunningRight')
                self.velocity = (speed, 0)
            else:
                self.set_state('RunningLeft')
                self.velocity = (speed * -1, 0)
        else:
            self.set_state('Standing')
            self.velocity = (0, 0)
                

# the noarms letters sprite
class Letter(pygame.sprite.Sprite):
    
    fall = pygame.mixer.Sound(os.path.join('namm', 'sounds', 'NoArmsIntro', 'FallingBomb.wav'))
    secure = pygame.mixer.Sound(os.path.join('namm', 'sounds', 'NoArmsIntro', 'LevelBonus.wav'))
    
    def __init__(self, init_pos, file_name, init_color):
        pygame.sprite.Sprite.__init__(self, self.groups)    
        self.image = pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', file_name))
        self.image = self.image.convert(8)
        self.image.set_colorkey(self.image.get_at((0, 0)), RLEACCEL)
        self.fall = Letter.fall
        self.secure = Letter.secure
        self.pos = init_pos
        self.color = init_color
        self.rect = self.image.get_rect()
        self.velocity = (0, 0)
        self.state = 'Still'

        self.targetX = None
        self.targetY = None

    def update(self):
        self.pos = (self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1])
        if ((self.state == 'MovingLeft' and self.pos[0] <= self.targetX) or
                (self.state == 'MovingRight' and self.pos[0] >= self.targetX)):
            self.pos = (self.targetX, self.pos[1])
            self.velocity = (0, 0)
            self.state = 'Still'
        if ((self.state == 'MovingUp' and self.pos[1] <= self.targetY) or
                (self.state == 'MovingDown' and self.pos[1] >= self.targetY)):
            self.pos = (self.pos[0], self.targetY)
            self.velocity = (0, 0)
            self.state = 'Still'
            self.secure.play()

        self.rect.center = self.pos
        self.image.set_palette_at(1, self.color)

    def move_to_x(self, new_x, speed):
        if new_x != self.pos[0]:
            self.targetX = new_x
            if new_x > self.pos[0]:
                self.state = 'MovingRight'
                self.velocity = (speed, 0)
            else:
                self.state = 'MovingLeft'
                self.velocity = (speed * -1, 0)
        else:
            self.state = 'Still'
            self.velocity = (0, 0)

    def move_to_y(self, new_y, speed):
        # assuming programmer will move to either x or y, not both!
        if new_y != self.pos[1]:
            self.targetY = new_y
            if new_y > self.pos[1]:
                self.state = 'MovingDown'
                self.velocity = (0, speed)
                self.fall.play()
            else:
                self.state = 'MovingUp'
                self.velocity = (0, speed * -1)
        else:
            self.state = 'Still'
            self.velocity = (0, 0)


# the title text sprite
class TitleText(pygame.sprite.Sprite):
    def __init__(self, init_pos, file_name):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', file_name))
        self.image = self.image.convert()
        self.pos = init_pos
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = self.pos


# the opening screen sprites
class OpeningObjects(pygame.sprite.Sprite):
    def __init__(self, init_pos, file_name, color_key_flag):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.image.load(os.path.join('namm', 'images', 'NoArmsIntro', file_name))
        self.image = self.image.convert()
        if color_key_flag == 1:
            self.image.set_colorkey(self.image.get_at((0, 0)), RLEACCEL)
        self.pos = init_pos
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = self.pos
