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
            print(k, f"{k.base_weight * 100:.8f}%")
            for i in v:
                print("-", i)
            print("\n")

    def add_item(self, *item):
        for i in item:
            self.items.append(i)
            if i.rarity not in self.rarity_map:
                self.rarity_map[i.rarity] = []
            self.rarity_map[i.rarity].append(i)

    def _fill_flex_rarity(self):
        rarities = list(self.rarity_map.keys())
        total_weight = sum([r.base_weight for r in rarities])
        flex_count = sum([isinstance(r, FlexRarity) for r in rarities])

        if any([r.base_weight < 1 for r in rarities]) and any([isinstance(r, FlexRarity) for r in rarities]):
            for r in rarities:
                if isinstance(r, FlexRarity):
                    r.base_weight = (1 - total_weight) / flex_count
        else:
            raise ValueError(f"Total Weight {total_weight} (Should Be Equal to 1) and No FlexRarity found.")

    @abstractmethod
    def _draw(self):
        pass

    def pre_draw(self):
        pass

    def draw(self, start_draw_count: int = 0, draw_count: int = 1):
        self._fill_flex_rarity()
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


class FlexRarity(GachaRarityBase):
    def __init__(self, name):
        super().__init__(name)
        self.base_weight = 0
