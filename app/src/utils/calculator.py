"""
Formulas relating to player experience/drops
Source: https://pathofexile.gamepedia.com/Experience
"""


class PlayerRateCalculator:
    """
    Has calculations related to player gains
    """

    def __init__(self):
        self.player_level = 0
        self.monster_level = 0

    def set_levels(self, player_level, monster_level):
        self.player_level = player_level
        self.monster_level = monster_level

    def get_penalties(self):
        """
        Gets the calculated drop and exp penalty values based on the level
        values given.
        """
        if self.player_level > 0 and self.monster_level > 0:
            penalty_data = {
                'drop_penalty': self.calc_drop_penalty(),
                'exp_penalty': self.calc_exp_penalty()
            }
            return penalty_data
        else:
            return None

    def calc_drop_penalty(self):
        """
        Penalty applies to the chance of currency items and divination cards.
        Applies to areas with a monster level more than two levels lower than
        your character level.

        dropPenalty = 2.5% * (LvlChar - (LvlMonster + 2))
        """
        player_level = min(self.player_level, 68)
        monster_level = self.area_level

        drop_penalty = 0.025 * (player_level - (monster_level + 2))

        return drop_penalty

    def calc_exp_penalty(self):
        """
        Calculates the multiplier applied to the raw experience

        XPMultiplier = max(
        ((PlayerLevel + 5)/(PlayerLevel + 5 + EffectiveDifference^2.5))^1.5,
        0.01)
        """
        level = self.player_level
        effective_diff = self._effective_difference()

        level_val = (level + 5) / (level + 5 + effective_diff ** 2.5)
        xp_multiplier = max(level_val, 0.01)

        return xp_multiplier

    def _safe_zone(self):
        """
        Calculates safe zone number. The number corresponds to safe level
        ranges where no experience penalty is applied

        SafeZone = floor()
        =====  =========
        Level  Safe Zone
        =====  =========
        1-15   3
        16-31  4
        32-47  5
        48-63  6
        64-79  7
        80-95  8
        96+    9
        =====  =========
        """
        player_level = self.player_level

        safe_zone = 3 + player_level // 16

        return safe_zone

    def _effective_difference(self):
        """
        Calculates the effective level difference, any additional level
        difference in excess of the safe ranges

        EffectiveDifference = max(|PlayerLevel - MonsterLevel| - safeZone, 0)
        """
        player_level = self.player_level
        monster_level = self.monster_level
        safe_zone = self.safe_zone

        level_difference = abs(player_level - monster_level)
        effective_difference = max(level_difference - safe_zone, 0)

        return effective_difference
