import geopandas as gpd
import matplotlib.pyplot as plt

# 读取世界地图
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# datas: dict[国家名, 权重]
import pandas as pd
datas = {'China': 120, 'United States': 100, 'India': 80}

df = pd.DataFrame(list(datas.items()), columns=['name', 'Value'])

# 合并数据
world = world.merge(df, how='left', left_on='name', right_on='name')

# 绘制 choropleth
fig, ax = plt.subplots(1, 1, figsize=(20, 10))
world.plot(column='Value', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='0.8', missing_kwds={'color': 'lightgrey'})
plt.show()
