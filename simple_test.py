import matplotlib.pyplot as plt

from gacha import GachaRarity, SimpleGacha

# 定义稀有度
common = GachaRarity("Common", 0.5)
rare = GachaRarity("Rare", 0.3)
epic = GachaRarity("Epic", 0.15)
legendary = GachaRarity("Legendary", 0.05)

# 创建SimpleGacha实例并添加项目
gacha = SimpleGacha()
gacha.add_item("C Sword", common)
gacha.add_item("C Shield", common)
gacha.add_item("R Spear", rare)
gacha.add_item("R Armor", rare)
gacha.add_item("E Magic Staff", epic)
gacha.add_item("L Dragon", legendary)

# 进行多次抽取并记录结果
results = {}
for _ in range(10000):  # 假设我们抽了10000次
    result = gacha.draw()
    if result in results:
        results[result] += 1
    else:
        results[result] = 1

# 绘制饼图展示结果
plt.figure(figsize=(10, 8))
plt.pie(results.values(), labels=results.keys(), autopct='%1.1f%%')
plt.title("Gacha Draw Results Distribution")
plt.show()
