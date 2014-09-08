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

from namm.darts import *

ATW_VARIATION_DUBS = "Doubles Only"
ATW_VARIATION_SKIP = "Skip'n'Jump"
ATW_VARIATION_DUBOUT = "Double-Out"
ATW_VARIATION_SHANG = "Shanghai"


class AroundTheWorld(Darts.Game):

    def __init__(self):
        super(AroundTheWorld, self).__init__("Around The World")
        self._playerOptions = [1,2,3,4]
        self._variationOptions.append(ATW_VARIATION_DUBS)
        self._variationOptions.append(ATW_VARIATION_SKIP)
        self._variationOptions.append(ATW_VARIATION_DUBOUT)
        self._variationOptions.append(ATW_VARIATION_SHANG)
        self._variation = Darts.GAME_VARIATION_STD

    @property
    def variation(self):
        return self._variation

    @variation.setter
    def variation(self, value):
        if value in self._variationOptions:
            self._variation = value #TODO: Only allow setter when state stopped?

    @property
    def instructions(self):
        instr = {}

        instr[Darts.INSTR_SUMMARY] = []
        instr[Darts.INSTR_SUMMARY].append("Also known as 'Round the Clock'")
        instr[Darts.INSTR_SUMMARY].append("Number of Players: any")
        instr[Darts.INSTR_SUMMARY].append("Darts per Round: 3")
        instr[Darts.INSTR_SUMMARY].append("An easy, fast and fun game that helps to develop accuracy.")
        
        instr[Darts.INSTR_OBJECT] = []
        instr[Darts.INSTR_OBJECT].append("Be the first player to hit all the numbers on the board, in order.")

        instr[Darts.INSTR_GAMEPLAY] = []
        instr[Darts.INSTR_GAMEPLAY].append("Each player throws 3 darts per round.")
        instr[Darts.INSTR_GAMEPLAY].append("Players begin throwing at the 1.  After a player hits the 1, that player throws at the 2 next, then the 3, and so on.")
        instr[Darts.INSTR_GAMEPLAY].append("Singles, doubles and triples all count the same.")
        instr[Darts.INSTR_GAMEPLAY].append("Each new round, players pick up where they left off in the previous round.")
        instr[Darts.INSTR_GAMEPLAY].append("The first player to hit all the numbers in order from 1-20 wins.")

        instr[Darts.INSTR_SCORING] = []
        instr[Darts.INSTR_SCORING].append("No Arms Darts awards 1 point for each target number hit.")

        instr[Darts.INSTR_VARIATIONS] = []
        instr[Darts.INSTR_VARIATIONS].append("Skip'n'Jump: Same as the standard rules, except doubles skip the next number and triples skip the next 2 numbers.")
        instr[Darts.INSTR_VARIATIONS].append("Double-out: Same as the standard rules, except players must hit the double ring when shooting for 20.")
        instr[Darts.INSTR_VARIATIONS].append("Doubles Only: Same as the standard rules, except players must hit the double ring for all numbers.")
        instr[Darts.INSTR_VARIATIONS].append("Shanghai: Same as the standard rules, except players must hit a single, double and triple of each number before moving to the next.")

        return instr

    def zeroScores(self):
        super(AroundTheWorld, self).zeroScores()
        for player in self.players:
            player.targetWedgeValue = 1
            setPlayerTargetRingValues(player)

    def setPlayerTargetRingValues(self, player):
        if (self._variation == ATW_VARIATION_DUBS) or ((self._variation == ATW_VARIATION_DUBOUT) and player.targetWedgeValue == 20):
            player.targetRingValues = [2]
        elif (self._variation == ATW_VARIATION_SHANG):
            player.targetRingValues = [1,2,3]
        else:
            player.targetRingValues = [1,2,3]

    def scorePlayerThrow(self, playerName, throw):
        super(AroundTheWorld, self).scorePlayerThrow(playerName, throw)
        if throw:
            hitTarget = ((throw.wedgeValue == self._players[playerName].targetWedgeValue)
                         and (throw.ringValue in self._players[playerName].targetRingValues))
            hitOut = hitTarget and ((throw.wedgeValue == 20 and ((self._variation != ATW_VARIATION_DUBOUT)
                                                        or ((self._variation == ATW_VARIATION_DUBOUT) and throw.ringValue == 2)))
                      or ((self._variation == ATW_VARIATION_SKIP) and ((throw.wedgeValue == 19 and (throw.ringValue == 2
                                                                                    or ((self._variation != ATW_VARIATION_DUBOUT) and throw.ringValue == 3)))
                                                       or (throw.wedgeValue == 18 and ((self._variation != ATW_VARIATION_DUBOUT) and throw.ringValue == 3)))))
            if hitOut:
                self._players[playerName].targetWedgeValue = None
                self.winner = _players[playerName]
                self._state = GameState(Darts.STATE_GAMEOVER)
            elif hitTarget:
                if self.jumpAndSkipRings:
                    self._players[playerName].targetWedgeValue += throw.ringValue
                else:
                    self._players[playerName].targetWedgeValue += 1

                if self._players[playerName].targetWedgeValue >= 20:
                    self._players[playerName].targetWedgeValue = 20
