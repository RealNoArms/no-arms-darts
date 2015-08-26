"""
No Arms Many Mediums Common Utilities Module

    Copyright (C) 2013, 2014, 2015  Tim Kracht <timkracht4@gmail.com>

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

from itertools import chain


# math utilities
def wrap_increment(n, m):
    return (n + 1) % m


# text utilities
def trunc_line(text, font, max_width):
        real = len(text)
        s_text = text
        l = font.size(text)[0]
        cut = 0
        a = 0
        done = 1

        while l > max_width:
            a += 1
            n = text.rsplit(None, a)[0]
            if s_text == n:
                cut += 1
                s_text = n[:-cut]
            else:
                s_text = n
            l = font.size(s_text)[0]
            real = len(s_text)
            done = 0
        return real, done, s_text


def wrap_line(text, font, max_width):
    done = 0
    wrapped = []

    while not done:
        nl, done, s_text = trunc_line(text, font, max_width)
        wrapped.append(s_text.strip())
        text = text[nl:]
    return wrapped


def wrap_multi_line(text, font, max_width):
    """ returns text taking new lines into account.
    """
    lines = chain(*(wrap_line(line, font, max_width) for line in text.splitlines()))
    return list(lines)
