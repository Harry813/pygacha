import random

from gacha import GachaPoolBase, GachaItem, GachaRarityBase, FlexRarity


class PRDGTRarity(GachaRarityBase):
    def __init__(self, name, a: int, b: int, p_star: float, p_delta: float, priority: int = 0):
        """
        伪随机保底抽卡稀有度，基于PRDGT算法。设抽取次数为T时：
        1. 当T < a时，概率为p_star；
        2. 当a < T < b时，概率为p_star + (T - a) * p_delta
        3. 当T > b时，概率为1。

        优先度高的稀有度会先被抽取。

        :param name: 稀有度名称
        :param a: 抽取范围最小阈值
        :param b: 抽取范围最大阈值
        :param p_star: 基础概率
        :param p_delta: 概率增量
        """
        super().__init__(name, priority)
        self.a = a
        self.b = b
        self.p_star = p_star
        self.p_delta = p_delta

        self._draw_count = 0
        self._adjust_weight = 0
        self._change_flag = False

    @property
    def weight(self):
        if self._change_flag:
            return self._adjust_weight

        if self.draw_count < self.a:
            return self.p_star
        elif self.a < self.draw_count < self.b:
            return self.p_star + (self.draw_count - self.a) * self.p_delta
        else:
            return 1

    @weight.setter
    def weight(self, value):
        self._adjust_weight = value
        self._change_flag = True

    @property
    def draw_count(self):
        return self._draw_count

    @draw_count.setter
    def draw_count(self, value):
        self._draw_count = value
        self._change_flag = False


class PRDGTItem(GachaItem):
    def __init__(self, name, rarity: PRDGTRarity | FlexRarity, inst=None, adjusted_modifier=0, is_guaranteed=0):
        super().__init__(name, rarity, inst, adjusted_modifier)
        self.is_guaranteed = is_guaranteed


class PRDGTGacha(GachaPoolBase):
    def __init__(self):
        super().__init__()

        self.total_draw = 0
        self.count_from_last_rarity = {}  # 距离上一次抽到该稀有度的物品的抽取次数
        self.count_from_last_gtitem = {}  # 距离上一个抽取到的保底物品的抽取次数

    def add_item(self, *item):
        guaranteed_count = []

        for i in item:
            if i.is_guaranteed:
                if i.rarity in guaranteed_count:
                    raise ValueError(f"{i.rarity} has more than one guaranteed item")
                guaranteed_count.append(i.rarity)
                self.count_from_last_gtitem[i] = 0
            self.items.append(i)

            if i.rarity not in self.rarity_map:
                self.rarity_map[i.rarity] = []
            self.rarity_map[i.rarity].append(i)

            if i.rarity not in self.count_from_last_rarity:
                self.count_from_last_rarity[i.rarity] = 0

            if i.is_guaranteed > 0 and i not in self.count_from_last_gtitem:
                self.count_from_last_gtitem[i] = 0

    def load_rec(self, *item):
        for i in item:
            for rarity in self.count_from_last_rarity:
                if rarity < i.rarity:
                    self.count_from_last_rarity[rarity] = 0
                elif rarity > i.rarity:
                    self.count_from_last_rarity[rarity] += 1

            if i in self.count_from_last_gtitem and i.is_guaranteed > 0:
                self.count_from_last_gtitem[i] = 0
                self.total_draw = 0
            else:
                for gt_item in self.count_from_last_gtitem:
                    if i.rarity == gt_item.rarity:
                        if i != gt_item:
                            self.count_from_last_gtitem[gt_item] += 1
                        else:
                            self.count_from_last_gtitem[gt_item] = 0

    def _draw_rarity(self):
        rarity_weights = {}
        adjusted_weights = {}
        for rarity in self.rarity_map.keys():
            rarity_weights[rarity] = rarity.calculate_weight(self.count_from_last_rarity[rarity])

        total_weight = sum(rarity_weights.values())
        if total_weight >= 1:
            rest_weight = 1
            sorted_rarity_weights = sorted(rarity_weights.items(), key=lambda x: x[0].priority, reverse=True)
            for rarity, weight in sorted_rarity_weights:
                if weight >= 1:
                    return rarity
                elif rest_weight == 0:
                    adjusted_weights[rarity] = 0
                else:
                    if weight > rest_weight:
                        adjusted_weights[rarity] = rest_weight
                        break
                    else:
                        rest_weight -= weight
                        adjusted_weights[rarity] = weight
            else:
                raise ValueError("No rarity selected")
        else:
            pick = random.uniform(0, total_weight)
            current = 0
            for rarity, adjusted_weight in adjusted_weights.keys():
                current += adjusted_weight
                if current >= pick:
                    return rarity

    def _draw_item(self, rarity):
        for r in self.count_from_last_rarity:
            if r < rarity:
                self.count_from_last_rarity[r] = 0

        for i in self.count_from_last_gtitem:
            if i.rarity == rarity and self.count_from_last_gtitem[i] >= i.is_guaranteed:
                self.count_from_last_gtitem[i] = 0
                return i
        else:
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
