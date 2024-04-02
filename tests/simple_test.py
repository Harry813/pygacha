import matplotlib.pyplot as plt

from gacha import SimpleRarity, SimpleGacha
from gacha.base import GachaItem

# 定义稀有度
common = SimpleRarity("Common", 0.5)
rare = SimpleRarity("Rare", 0.3)
epic = SimpleRarity("Epic", 0.15)
legendary = SimpleRarity("Legendary", 0.05)

sword_c = GachaItem("C Sword", common, "Sword", adjusted_modifier=0.8)
shield_c = GachaItem("C Shield", common, "Shield")
spear_r = GachaItem("R Spear", rare, "Spear")
armor_r = GachaItem("R Armor", rare, "Armor")
staff_e = GachaItem("E Magic Staff", epic, "Staff")
dragon_l = GachaItem("L Dragon", legendary, "Dragon")

# 创建SimpleGacha实例并添加项目
gacha = SimpleGacha()
gacha.add_item(sword_c, shield_c, spear_r, armor_r, staff_e, dragon_l)

# 进行多次抽取并记录结果
statics = {}
results = gacha.draw(draw_count=100000)
for r in results:
    if r['item'].name not in statics:
        statics[r['item'].name] = 1
    else:
        statics[r['item'].name] += 1

# 绘制饼图展示结果
plt.figure(figsize=(10, 8))
plt.pie(statics.values(), labels=statics.keys(), autopct='%1.1f%%')
plt.title("Gacha Draw Results Distribution")
plt.show()
