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


# TODO: logging
class AroundTheWorld(Darts.Game):

    def __init__(self):
        super(AroundTheWorld, self).__init__("Around The World")
        self._playerOptions = [1, 2, 3, 4]
        self._variationOptions.append(ATW_VARIATION_DUBS)
        self._variationOptions.append(ATW_VARIATION_SKIP)
        self._variationOptions.append(ATW_VARIATION_DUBOUT)
        self._variationOptions.append(ATW_VARIATION_SHANG)
        self._variation = Darts.GAME_VARIATION_STD
        self._settingOptions = None

    @property
    def variation(self):
        return self._variation

    @variation.setter
    def variation(self, value):
        if value in self._variationOptions:
            self._variation = value  # TODO: Only allow setter when state stopped?

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
        instr[Darts.INSTR_GAMEPLAY].append("Players begin throwing at the 1.  After a player hits the 1, that player"
                                           " throws at the 2 next, then the 3, and so on.")
        instr[Darts.INSTR_GAMEPLAY].append("Singles, doubles and triples all count the same.")
        instr[Darts.INSTR_GAMEPLAY].append("Each new round, players pick up where they left off in the previous round.")
        instr[Darts.INSTR_GAMEPLAY].append("The first player to hit all the numbers in order from 1-20 wins.")

        instr[Darts.INSTR_SCORING] = []
        instr[Darts.INSTR_SCORING].append("No Arms Darts awards 1 point for each target number hit.")

        instr[Darts.INSTR_VARIATIONS] = []
        instr[Darts.INSTR_VARIATIONS].append("Skip'n'Jump: Same as the standard rules, except doubles skip the next "
                                             "number and triples skip the next 2 numbers.")
        instr[Darts.INSTR_VARIATIONS].append("Double-out: Same as the standard rules, except players must hit the "
                                             "double ring when shooting for 20.")
        instr[Darts.INSTR_VARIATIONS].append("Doubles Only: Same as the standard rules, except players must hit the "
                                             "double ring for all numbers.")
        instr[Darts.INSTR_VARIATIONS].append("Shanghai: Same as the standard rules, except players must hit a single, "
                                             "double and triple of each number before moving to the next.")

        return instr

    def zero_scores(self):
        super(AroundTheWorld, self).zeroScores()
        for player in self.players:
            player.targetWedgeValue = 1
            self.set_player_target_ring_values(player)

    def set_player_target_ring_values(self, player):
        if self._variation == ATW_VARIATION_DUBS:
            player.targetRingValues = [2]
        else:
            player.targetRingValues = [1, 2, 3]

    def score_player_throw(self, player_name, throw):
        super(AroundTheWorld, self).score_player_throw(player_name, throw)
        if throw:
            hit_target = ((throw.wedgeValue == self._players[player_name].targetWedgeValue)
                          and (throw.ringValue in self._players[player_name].targetRingValues))
            hit_out = hit_target and ((throw.wedgeValue == 20 and
                                       ((self._variation != ATW_VARIATION_DUBOUT) or
                                        ((self._variation == ATW_VARIATION_DUBOUT) and throw.ringValue == 2))) or
                                      (self._variation == ATW_VARIATION_SHANG and throw.wedge_value == 20 and
                                       len(self._players[player_name].targetRingValues) == 1) or
                                      ((self._variation == ATW_VARIATION_SKIP) and
                                       ((throw.wedgeValue == 19 and (throw.ringValue == 2 or
                                                                     ((self._variation != ATW_VARIATION_DUBOUT) and
                                                                      throw.ringValue == 3))) or
                                        (throw.wedgeValue == 18 and ((self._variation != ATW_VARIATION_DUBOUT) and
                                                                     throw.ringValue == 3)))))
            if hit_out:
                self._players[player_name].targetWedgeValue = None
                self.winner = self._players[player_name]
                self._state = Darts.GameState(Darts.STATE_GAMEOVER)
            elif hit_target:
                if self._variation == ATW_VARIATION_SKIP:
                    self._players[player_name].targetWedgeValue += throw.ringValue
                elif self._variation == ATW_VARIATION_SHANG:
                    self._players[player_name].targetRingValues.remove(throw.ringValue)
                    if len(self._players[player_name].targetRingValues) == 0:
                        self._players[player_name].targetWedgeValue += 1
                        self._players[player_name].targetRingValues = [1, 2, 3]
                else:
                    self._players[player_name].targetWedgeValue += 1

                if self._players[player_name].targetWedgeValue >= 20:
                    self._players[player_name].targetWedgeValue = 20

                if self._variation == ATW_VARIATION_DUBOUT and self._players[player_name].targetWedgeValue == 20:
                    self._players[player_name].targetRingValues = [2]
