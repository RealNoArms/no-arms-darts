"""

Common Error Classes


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


# Base Error
class Error(Exception):

    def __init__(self, msg=None, obj=None):
        self._msg = msg
        self._obj = obj
        self._rep = "Error"

    def __str__(self):
        rep = self._rep
        if self._msg is not None:
            rep += ": " + self._msg

        rep += ": obj = "

        if self._obj is not None:
            rep += self._obj
        else:
            rep += "{None}"
        return rep