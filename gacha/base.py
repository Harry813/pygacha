from abc import ABC, abstractmethod


class GachaItem:
    def __init__(self, name, rarity: "GachaRarityBase", inst=None, adjusted_modifier=0):
        """
        :param name: 稀有度名称
        :param rarity: 稀有度类型
        :param inst: Item实例
        :param adjusted_modifier: 在总的稀有度中的比例。0表示不参与调整
        """
        self.name = name
        self.rarity = rarity
        self.inst = inst

        self.adjusted_weight = 0
        self.adjusted_modifier = adjusted_modifier

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
        self.rarity_map = {}

    def show_items(self):
        for k, v in self.rarity_map.items():
            print(k)
            for i in v:
                print("-", i)

    def add_item(self, *item):
        for i in item:
            self.items.append(i)
            if i.rarity not in self.rarity_map:
                self.rarity_map[i.rarity] = []
            self.rarity_map[i.rarity].append(i)

    @abstractmethod
    def _draw(self):
        pass

    def pre_draw(self):
        pass

    def draw(self, start_draw_count: int = 0, draw_count: int = 1):
        self.pre_draw()

        self.draw_count = start_draw_count
        results = []
        for _ in range(draw_count):
            self.draw_count += 1
            results.append({
                'id': self.draw_count,
                'item': self._draw()
            })
        return results
