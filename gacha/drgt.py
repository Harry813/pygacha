from gacha import GachaPoolBase


class DRGTRarity:
    def __init__(self, name, A, B, delta_p):
        """
        :param name: 稀有度名称
        :param A: 最小保底次数
        :param B: 最大保底次数
        :param delta_p: 最小保底次数概率增量
        """
        self.name = name
        self.A = A
        self.B = B
        self.delta_p = delta_p

    @property
    def expected_draw(self):
        return self.A + (1 - (1 - self.delta_p) ** (self.B - self.A)) / self.delta_p


class DRGTGacha(GachaPoolBase):
    def _draw(self):
        pass
