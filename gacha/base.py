import random
from abc import ABC, abstractmethod


class GachaRarity:
    def __init__(self, name, base_weight: float):
        self.name = name
        self.base_weight = base_weight


class GachaPool(ABC):
    def __init__(self):
        self.items = []

    def add_item(self, item, rarity):
        self.items.append((item, rarity))

    @abstractmethod
    def draw(self):
        pass



