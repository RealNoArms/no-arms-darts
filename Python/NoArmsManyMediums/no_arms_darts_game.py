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

import sys
import pygame


pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
displayInfo = pygame.display.Info()

try:
    screen = pygame.display.set_mode((displayInfo.current_w, displayInfo.current_h),
                                     pygame.FULLSCREEN | pygame.HWSURFACE, 32)
    from namm import no_arms_darts
    dartsGame = no_arms_darts.NoArmsDarts(screen, "Warn")
    # print "running darts"
    dartsGame.run()
except Exception, e:
    print e
finally:
    pygame.quit()
    sys.exit()
