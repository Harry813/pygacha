from abc import ABC, abstractmethod


class GachaItem:
    def __init__(self, name, rarity: "GachaRarityBase", inst=None):
        """
        :param name:
        :param rarity: 稀有度
        :param inst:
        """
        self.name = name
        self.rarity = rarity
        self.inst = inst

        self.adjusted_weight = 0

    def __str__(self):
        return f"{self.name}({self.rarity})"


class GachaRarityBase(ABC):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class GachaPoolBase(ABC):
    def __init__(self):
        self.items = []
        self.draw_count = 0

    def _adjust_weights(self):
        rarity_counts = {}
        for item in self.items:
            if item.rarity.name not in rarity_counts:
                rarity_counts[item.rarity.name] = 1
            else:
                rarity_counts[item.rarity.name] += 1

        for item in self.items:
            item.adjusted_weight = item.rarity.base_weight / rarity_counts[item.rarity.name]

    def add_item(self, *item):
        for i in item:
            self.items.append(i)

    @abstractmethod
    def _draw(self):
        pass

    def draw(self, start_draw_count: int = 0, draw_count: int = 1):
        self._adjust_weights()
        self.draw_count = start_draw_count
        results = []
        for _ in range(draw_count):
            self.draw_count += 1
            results.append({
                'id': self.draw_count,
                'item': self._draw()
            })
        return results
