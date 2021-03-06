"""

Classes in the Base Darts model


    Copyright (C) 2013-2014  Tim Kracht <timkracht4@gmail.com>

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

from namm.common.error import Error
# from namm.common.logger import Logger

# package-level stuff
WEDGE_NAMES = {"1": "1",
               "2": "2",
               "3": "3",
               "4": "4",
               "5": "5",
               "6": "6",
               "7": "7",
               "8": "8",
               "9": "9",
               "10": "10",
               "11": "11",
               "12": "12",
               "13": "13",
               "14": "14",
               "15": "15",
               "16": "16",
               "17": "17",
               "18": "18",
               "19": "19",
               "20": "20",
               "25": "Bullseye"}

WEDGE_VALUES = {"1": 1,
                "2": 2,
                "3": 3,
                "4": 4,
                "5": 5,
                "6": 6,
                "7": 7,
                "8": 8,
                "9": 9,
                "10": 10,
                "11": 11,
                "12": 12,
                "13": 13,
                "14": 14,
                "15": 15,
                "16": 16,
                "17": 17,
                "18": 18,
                "19": 19,
                "20": 20,
                "25": 25}

RING_NAMES = {"S": "Single",
              "I": "Inner Single",
              "O": "Outer Single",
              "D": "Double",
              "T": "Triple"}

RING_VALUES = {"S": 1,
               "I": 1,
               "O": 1,
               "D": 2,
               "T": 3}

# States
STATE_PLAYING = "Playing"
STATE_STOPPED = "Stopped"
STATE_PAUSED = "Paused"
STATE_GAMEOVER = "Game Over"

# Instructions
INSTR_SUMMARY = "Instructions Summary"
INSTR_OBJECT = "Instructions Object"
INSTR_SCORING = "Instructions Scoring"
INSTR_GAMEPLAY = "Instructions Game Play"
INSTR_VARIATIONS = "Instructions Variations"

# Standard Variation
GAME_VARIATION_STD = "Standard"

# TODO: Go!!!!!

# common Darts functions
def get_wedge_name(code):
    if code is not None and code in WEDGE_NAMES:
        return WEDGE_NAMES[code]
    else:
        raise ParameterError("Invalid wedge!", code)


def get_wedge_value(code):
    if code is not None and code in WEDGE_VALUES:
        return WEDGE_VALUES[code]
    else:
        raise ParameterError("Invalid wedge!", code)


def get_ring_name(code):
    if code is not None and code in RING_NAMES:
        return RING_NAMES[code]
    else:
        raise ParameterError("Invalid ring!", code)


def get_ring_value(code):
    if code is not None and code in RING_VALUES:
        return RING_VALUES[code]
    else:
        raise ParameterError("Invalid ring!", code)


def is_valid_wedge(code):
    return code in WEDGE_NAMES


def is_valid_ring(code):
    return code in RING_NAMES


# TODO: logging
# basic dart game
class Game(object):

    def __init__(self, name):
        self._name = name
        self._playerOptions = []
        self._variationOptions = []
        self._variationOptions.append(GAME_VARIATION_STD)
        self._settingOptions = []
        self._state = None
        self._winner = None

        self._minPlayers = 1
        self._maxPlayers = 4
        # self.numPlayers = 1
        self._throwsPerTurn = 3
        self._roundsPerLeg = None
        self._legsPerSet = 1
        self._setsPerMatch = 1

        self._variation = None
        self._settings = None

        self._players = None
        self._currentPlayerName = None
        self._currentThrow = 0
        self._currentRound = 0
        self._currentLeg = 0
        self._currentSet = 0

        self.reset()
        
    def __str__(self):
        return self._name

    def start(self):
        if self._state is not None and self._state.name == STATE_STOPPED:
            self._winner = None
            self.zero_scores()
            self._state = GameState(STATE_PLAYING)
        else:
            raise GameStateError("Cannot start, game state is not stopped!", self._state)

    def stop(self):
        self._state = GameState(STATE_STOPPED)

    def score_player_throw(self, player_name, throw):
        if self._state is not None and self._state.name == STATE_PLAYING:
            if player_name in self._players:
                self._players[player_name].append(throw)
            else:
                raise ParameterError("Cannot score throw, unknown player name!", player_name)
        else:
            raise GameStateError("Cannot score throw, game state is not playing!", self._state)

    def zero_scores(self):
        for player in self.players:
            player.points = 0
    
    def reset(self):
        self._minPlayers = 1
        self._maxPlayers = 4
        # self.numPlayers = 1
        self._throwsPerTurn = 3
        self._roundsPerLeg = None
        self._legsPerSet = 1
        self._setsPerMatch = 1
        
        self._players = {}
        self._currentPlayerName = None
        self._currentThrow = 0
        self._currentRound = 0
        self._currentLeg = 0
        self._currentSet = 0

        self._state = GameState(STATE_STOPPED)
        self._winner = None

    def game_menu(self, screen, background, font, log_level):
        raise DartsNotImplementedError("No Menu Set!", self)

    # Properties
    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state
    
    @property
    def num_players(self):
        if self._players is not None:
            return len(self._players)
        else:
            return 0

    @property
    def instructions(self):
        raise DartsNotImplementedError("No game instructions!", None)

    @property
    def options(self):
        return {'Players': self._playerOptions,
                'Variations': self._variationOptions,
                'Settings': self._settingOptions}

    @property
    def player_options(self):
        return self._playerOptions

    @property
    def setting_options(self):
        return self._settingOptions

    @property
    def variation_options(self):
        return self._variationOptions

    @property
    def players(self):
        if self._players is not None:
            return self._players.viewvalues()
        else:
            return None

    @players.setter
    def players(self, player_list):
        self._players.clear()
        if player_list is not None and len(player_list) > 0:
            for player in player_list:
                if player.name in self._players:
                    raise ParameterError("List of players contains duplicate player names!", player_list)
                else:
                    self._players[player.name] = player

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, value):
        if value in self._settingOptions:
            self._settings = value
        else:
            raise ParameterError("Invalid Game settings!", value)

    @property
    def variation(self):
        return self._variation

    @variation.setter
    def variation(self, value):
        if value in self._variationOptions:
            self._variation = value
        else:
            raise ParameterError("Invalid Game variation!", value)


# represents a basic darts player
class Player(object):
    def __init__(self, name=None):
        self.name = name
        self.points = 0
        self.throws = []
        self.targetRingValues = []
        self.targetWedgeValue = None
        
    def __str__(self):
        return self.name


# represents a state of the game
class GameState(object):
    def __init__(self, state_name):
        self.name = state_name

    def __str__(self):
        return self.name


# Represents a wedge and ring combination, as in the result of a dart throw
class Throw(object):
    
    def __init__(self, rng, wdg):
        self._wedge = None
        self._ring = None
        self.set_throw(rng, wdg)

    def __str__(self):
        rep = self.ring_name
        wdg = self.wedge_name

        if rep is not None and wdg is not None:
            rep += " " + wdg
        elif rep is not None or wdg is not None:
            rep = "Incomplete throw, missing wedge or ring"
        else:
            rep = "miss"
        return rep

    @property
    def wedge_name(self):
        return get_wedge_name(self.wedge)

    @property
    def ring_name(self):
        return get_ring_name(self.ring)
    
    @property
    def wedge_value(self):
        return get_wedge_value(self.wedge)

    @property
    def ring_value(self):
        return get_ring_value(self.ring)

    @property
    def points(self):
        if self.wedge is not None and self.ring is not None:
            return get_ring_value(self.ring) * get_wedge_value(self.wedge)
        else:
            raise Error("Incomplete throw, missing wedge or ring", (self.ring, self.wedge))

    @property
    def wedge(self):
        return self._wedge

    @wedge.setter
    def wedge(self, value):
        self._wedge = None
        if is_valid_wedge(value):
            self._wedge = value
        else:
            raise ParameterError("Invalid Wedge value!", value)
        
    @property
    def ring(self):
        return self._ring

    @ring.setter
    def ring(self, value):
        self._ring = None
        if is_valid_ring(value):
            self._ring = value
        else:
            raise ParameterError("Invalid Ring value!", value)

    def set_throw(self, rng, wdg):
        self.ring = rng
        self.wedge = wdg


# Errors
# Base Dart Error
class DartsError(Error):

    def __init__(self, msg=None, obj=None):
        super(DartsError, self).__init__(msg, obj)
        self._rep = "Darts Error"


# Invalid parameter
class ParameterError(DartsError):

    def __init__(self, msg=None, obj=None):
        super(ParameterError, self).__init__(msg, obj)
        self._rep = "Darts Parameter Error"


# Invalid game variation
class InvalidVariationError(DartsError):

    def __init__(self, msg=None, obj=None):
        super(InvalidVariationError, self).__init__(msg, obj)
        self._rep = "Darts Invalid Game Variation Error"


# Invalid game state
class GameStateError(DartsError):

    def __init__(self, msg=None, obj=None):
        super(GameStateError, self).__init__(msg, obj)
        self._rep = "Darts Game State Error"


# Not Implemented
class DartsNotImplementedError(DartsError):

    def __init__(self, msg=None, obj=None):
        super(DartsNotImplementedError, self).__init__(msg, obj)
        self._rep = "Darts Method Not Implemented Error"


if __name__ == "__main__":
    print("This module contains the base classes for Dart games.")
    input("\n\nPress enter to exit...")
