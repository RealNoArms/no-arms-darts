"""

The No Arms Many Mediums Common Events module


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


    Based on work by Shandy Brown, Paul Manta and Peter Cooner
        http://ezide.com/games/writing-games.html
        http://stackoverflow.com/questions/7249388/python-duck-typing-for-mvc-event-handling-in-pygame


"""
class WeakBoundMethod:
    def __init__(self, meth):
        import weakref
        self._self = weakref.ref(meth.__self__)
        self._func = meth.__func__

    def __call__(self, *args, **kwargs):
        self._func(self._self(), *args, **kwargs)

class EventManager:
    def __init__(self):
        self._listeners = { None : [ None ] }

    def add(self, eventClass, listener):
        print "add %s" % eventClass.__name__
        key = eventClass.__name__

        if (hasattr(listener, '__self__') and
            hasattr(listener, '__func__')):
            listener = WeakBoundMethod(listener)

        try:
            self._listeners[key].append(listener)
        except KeyError:
            self._listeners[key] = [listener]

        print "add count %s" % len(self._listeners[key])

    def remove(self, eventClass, listener):
        key = eventClass.__name__
        self._listeners[key].remove(listener)

    def post(self, event):
        eventClass = event.__class__
        key = eventClass.__name__
        print "post event %s (keys %s)" % (
            key, len(self._listeners[key]))
        for listener in self._listeners[key]:
            listener(event)

""" The Event base class """
class Event:
    def __init__(self):
        self.name = "Namm Event"
        self.data = None
