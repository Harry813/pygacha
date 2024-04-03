import random

from gacha import GachaPoolBase
from gacha.base import GachaRarityBase, GachaItem


class SimpleRarity(GachaRarityBase):
    def __init__(self, name, base_weight: float):
        super().__init__(name)
        self.base_weight = base_weight


class SimpleItem(GachaItem):
    def __init__(self, name, rarity: SimpleRarity, inst=None, adjusted_modifier=0):
        super().__init__(name, rarity, inst, adjusted_modifier)


class SimpleGacha(GachaPoolBase):
    def _draw_rarity(self):
        total_weight = sum(rarity.base_weight for rarity in self.rarity_map.keys())
        print(total_weight)
        pick = random.uniform(0, total_weight)
        current = 0
        for rarity in self.rarity_map.keys():
            current += rarity.base_weight
            if current >= pick:
                return rarity

    def _draw_item(self, rarity):
        items_of_rarity = [item for item in self.rarity_map[rarity]]
        total_modifier = sum(item.adjusted_weight for item in items_of_rarity)
        pick = random.uniform(0, total_modifier)
        current = 0
        for item in items_of_rarity:
            current += item.adjusted_weight
            if current >= pick:
                return item

    def pre_draw(self):
        for rarity, items in self.rarity_map.items():
            rest_weight = 1
            if sum([i.adjusted_modifier for i in items]) > 1:
                raise ValueError("Total adjusted modifier exceeds 1")

            modified_items = [i for i in items if i.adjusted_modifier > 0]
            not_modified_items = [i for i in items if i.adjusted_modifier == 0]

            for i in modified_items:
                i.adjusted_weight = i.adjusted_modifier
                rest_weight -= i.adjusted_modifier

            for i in not_modified_items:
                i.adjusted_weight = rest_weight / len(not_modified_items)

    def _draw(self):
        rarity = self._draw_rarity()
        print(rarity, end=" ")
        item = self._draw_item(rarity)
        print(item)
        return item
