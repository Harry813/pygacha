import random

from gacha import GachaPoolBase
from gacha.base import GachaRarityBase


class SimpleRarity(GachaRarityBase):
    def __init__(self, name, base_weight: float):
        super().__init__(name)
        self.base_weight = base_weight


class SimpleGacha(GachaPoolBase):
    def _draw(self):
        total_weight = sum(item.adjusted_weight for item in self.items)
        rand_val = random.uniform(0, total_weight)

        current_sum = 0
        for item in self.items:
            current_sum += item.adjusted_weight
            if rand_val <= current_sum:
                return item
        return None
