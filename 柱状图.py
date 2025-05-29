import matplotlib.pyplot as plt

from core import *

sos, pys = journal_statistics(load())
data = SliceableDict(sort_value(sos, reverse=False))[:10]

keys = list(data.keys())
values = list(data.values())

plt.figure(figsize=(8, 6))
plt.bar(keys, values, color='skyblue')
plt.title("垂直柱状图")
plt.xlabel("水果")
plt.ylabel("数量")
plt.xticks(rotation=90)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
