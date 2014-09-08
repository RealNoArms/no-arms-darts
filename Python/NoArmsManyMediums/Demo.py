"""

No Arms Many Mediums Demo

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

import sys, pygame
from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
displayInfo = pygame.display.Info()

try:
    screen = pygame.display.set_mode((displayInfo.current_w, displayInfo.current_h), pygame.FULLSCREEN | pygame.HWSURFACE, 32)
    import namm.intro.nammIntro
    intro = namm.intro.nammIntro.NammIntro(screen)
    intro.Run()
except:
    print "Uncool error"
finally:
    pygame.quit()
    sys.exit()
