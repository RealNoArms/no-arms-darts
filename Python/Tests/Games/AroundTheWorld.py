"""

Darts Games - Around The World


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

import Darts

class AroundTheWorld(Darts.Game):

    def __init__(self):
        super(AroundTheWorld, self).__init__("Around The World")
        self.jumpAndSkipRings = FALSE
        self._doublesOnly = FALSE
        self._shanghai = FALSE

    @property
    def doublesOnly(self):
        return self._doublesOnly

    @doublesOnly.setter
    def doublesOnly(self, value):
        self._doublesOnly = value
        if self.players:
            for player in self.players:
                setPlayerTargetRingValues(player)

    def instructions(self):
        instr = {}

        instr[INSTR_SUMMARY] = []
        instr[INSTR_SUMMARY].append("Around the World - also known as 'Round the Clock'")
        instr[INSTR_SUMMARY].append("Number of Players: any")
        instr[INSTR_SUMMARY].append("Darts per Round: 3")
        instr[INSTR_SUMMARY].append("An easy, fast and fun game that helps to develop accuracy.")
        
        instr[INSTR_OBJECT] = []
        instr[INSTR_OBJECT].append("Be the first player to hit all the numbers on the board, in order.")

        instr[INSTR_GAMEPLAY] = []
        instr[INSTR_GAMEPLAY].append("Each player throws 3 darts per round.")
        instr[INSTR_GAMEPLAY].append("Players begin throwing at the 1.  After a player hits the 1, that player throws at the 2 next, then the 3, and so on.")
        instr[INSTR_GAMEPLAY].append("Singles, doubles and triples all count the same.")
        instr[INSTR_GAMEPLAY].append("Each new round, players pick up where they left off in the previous round.")
        instr[INSTR_GAMEPLAY].append("The first player to hit all the numbers in order from 1-20 wins.")

        instr[INSRT_VARIATIONS] = []
        instr[INSRT_VARIATIONS].append("Skip'n'Jump: Same as the standard rules, except doubles skip the next number and triples skip the next 2 numbers.")
        instr[INSRT_VARIATIONS].append("Double-out: Same as the standard rules, except players must hit the double ring when shooting for 20.")
        instr[INSRT_VARIATIONS].append("Doubles Only: Same as the standard rules, except players must hit the double ring for all numbers.")
        instr[INSRT_VARIATIONS].append("Shanghai: Same as the standard rules, except players must hit a single, double and triple of each number before moving to the next.")

        return instr

    def zeroScores(self):
        super(AroundTheWorld, self).zeroScores()
        for player in self.players:
            player.targetWedgeValue = 1
            setPlayerTargetRingValues(player)

    def setPlayerTargetRingValues(self, player):
        if self._doublesOnly or (self.doubleOut and player.targetWedgeValue == 20):
            player.targetRingValues = [2]
        elif self._shanghai:
            player.targetRingValues = [1,2,3]
        else:
            player.targetRingValues = [1]

    def scorePlayerThrow(self, playerName, throw):
        super(AroundTheWorld, self).scorePlayerThrow(playerName, throw)
        if throw:
            hitTarget = ((throw.wedgeValue == self._players[playerName].targetWedgeValue)
                         and (throw.ringValue in self._players[playerName].targetRingValues))
            hitOut = hitTarget and ((throw.wedgeValue == 20 and (not _self.doubleOut
                                                        or (_self.doubleOut and throw.ringValue == 2)))
                      or ((self.jumpAndSkipRings) and ((throw.wedgeValue == 19 and (throw.ringValue == 2
                                                                                    or (not _self.doubleOut and throw.ringValue == 3)))
                                                       or (throw.wedgeValue == 18 and (not _self.doubleOut and throw.ringValue == 3)))))
            if hitOut:
                self._players[playerName].targetWedgeValue = None
                self.winner = _players[playerName]
                self._state = GameState(STATE_GAMEOVER)
            elif hitTarget:
                if self.jumpAndSkipRings:
                    self._players[playerName].targetWedgeValue += throw.ringValue
                else:
                    self._players[playerName].targetWedgeValue += 1

                if self._players[playerName].targetWedgeValue >= 20:
                    self._players[playerName].targetWedgeValue = 20
