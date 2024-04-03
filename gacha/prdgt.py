from gacha import GachaPoolBase, GachaItem, GachaRarityBase, FlexRarity


class PRDGTRarity(GachaRarityBase):
    def __init__(self, name, a: int, b: int, p_star: float, p_delta: float):
        super().__init__(name)
        self.a = a
        self.b = b
        self.p_star = p_star
        self.p_delta = p_delta

        self.draw_count = 0

    @property
    def weight(self):
        if self.draw_count < self.a:
            return self.p_star
        elif self.a < self.draw_count < self.b:
            return self.p_star + (self.draw_count - self.a) * self.p_delta
        else:
            return 1


class PRDItem(GachaItem):
    def __init__(self, name, rarity: PRDGTRarity | FlexRarity, inst=None, adjusted_modifier=0):
        super().__init__(name, rarity, inst, adjusted_modifier)


class PRDGacha(GachaPoolBase):
    def _draw_rarity(self):
        pass

    def _draw_item(self, rarity):
        pass

    def set_rec(self, rec):
        pass
