import matplotlib.pyplot as plt

data = {
    "苹果": 30,
    "香蕉": 45,
    "橙子": 10,
    "葡萄": 25
}

keys = list(data.keys())
values = list(data.values())

plt.figure(figsize=(8, 6))
plt.barh(keys, values, color='lightcoral')
plt.title("水平柱状图")
plt.xlabel("数量")
plt.ylabel("水果")
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
