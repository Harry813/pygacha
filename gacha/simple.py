import random

from gacha import GachaPool


class SimpleGacha(GachaPool):
    def draw(self):
        total_weight = sum(item[1].base_weight for item in self.items)
        rand_val = random.uniform(0, total_weight)
        current_sum = 0
        for item, rarity in self.items:
            current_sum += rarity.base_weight
            if rand_val <= current_sum:
                return item
        return None
