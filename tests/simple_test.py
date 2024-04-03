import matplotlib.pyplot as plt

from gacha import SimpleRarity, SimpleGacha
from gacha.base import GachaItem, FlexRarity
from gacha.simple import SimpleItem

# 定义稀有度
common = FlexRarity("Common")
rare = SimpleRarity("Rare", 0.3)
epic = SimpleRarity("Epic", 0.15)
legendary = SimpleRarity("Legendary", 0.05)

sword_c = SimpleItem("C Sword", common, "Sword", adjusted_modifier=0.8)
shield_c = SimpleItem("C Shield", common, "Shield")
spear_r = SimpleItem("R Spear", rare, "Spear")
armor_r = SimpleItem("R Armor", rare, "Armor")
staff_e = SimpleItem("E Magic Staff", epic, "Staff")
dragon_l = SimpleItem("L Dragon", legendary, "Dragon")

# 创建SimpleGacha实例并添加项目
gacha = SimpleGacha()
gacha.add_item(sword_c, shield_c, spear_r, armor_r, staff_e, dragon_l)
gacha.show_items()

# 进行多次抽取并记录结果
statics = {}
results = gacha.draw(draw_count=100000)
for r in results:
    if r['item'].name not in statics:
        statics[r['item'].name] = 1
    else:
        statics[r['item'].name] += 1

# 绘制饼图展示结果Q
plt.figure(figsize=(10, 8))
plt.pie(statics.values(), labels=statics.keys(), autopct='%1.1f%%')
plt.title("Gacha Draw Results Distribution")
plt.show()
