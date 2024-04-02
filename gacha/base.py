from abc import ABC, abstractmethod


class GachaItem:
    def __init__(self, name, rarity: "GachaRarityBase", inst=None, adjusted_modifier=0):
        """
        :param name:
        :param rarity: 稀有度
        :param inst:
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

    def _adjust_weights(self):
        rarity_modifier_totals = {}
        rarity_modifier_count = {}
        rarity_counts = {}

        # 计算每个稀有度下的物品数量及modifier总和
        for item in self.items:
            rarity_name = item.rarity.name
            if rarity_name not in rarity_modifier_totals:
                rarity_modifier_totals[rarity_name] = item.adjusted_modifier
                rarity_modifier_count[rarity_name] = 0
                rarity_counts[rarity_name] = 1
            else:
                rarity_modifier_totals[rarity_name] += item.adjusted_modifier
                rarity_counts[rarity_name] += 1

            if item.adjusted_modifier > 0:
                rarity_modifier_count[rarity_name] += 1

        print(rarity_modifier_totals, rarity_counts)
        for item in self.items:
            rarity_name = item.rarity.name
            if item.adjusted_modifier > 0:
                item.adjusted_weight = (item.rarity.base_weight * item.adjusted_modifier) / rarity_modifier_count[
                    rarity_name]
            else:
                remaining_weight = (1 - rarity_modifier_totals[rarity_name]) * item.rarity.base_weight
                item.adjusted_weight = remaining_weight / (rarity_counts[rarity_name] - rarity_modifier_count[rarity_name])

            print(str(item), item.adjusted_weight)

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
