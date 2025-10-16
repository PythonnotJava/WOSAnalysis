import plotly.express as px
import numpy as np
import pandas as pd

x, y = np.random.randn(100), np.random.randn(100)
z = 2*x - y + np.random.randn(100)*0.5
df = pd.DataFrame({'x': x, 'y': y, 'z': z})

fig = px.scatter_3d(df, x='x', y='y', z='z',
                    color='z', size=abs(df['z']), opacity=0.7)


fig.update_layout(title="三维数据分布图")
fig.show()
