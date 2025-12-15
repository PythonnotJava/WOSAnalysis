import plotly.express as pxexpress
import pandas

# datas是国家权重字典
def drawMapByDefine(
        datas: dict[str, int],
        width : int = 1600,
        height : int = 1000,
        scale : int = 3,
        colorMap : str = 'Turbo',
        title : str = '全球国家数据分布热力图'
) -> None:
    # 国家名称映射 (已处理常见不匹配)
    country_mapping = {
        'USA': 'United States of America',
        'England': 'United Kingdom',
        'Scotland': 'United Kingdom',
        'Wales': 'United Kingdom',
        'South Korea': 'Korea',
        'Dominican Rep': 'Dominican Republic',
        'Turkiye': 'Turkey',
        'Czech Republic': 'Czechia'
    }

    # 转DataFrame
    df = pandas.DataFrame(list(datas.items()), columns=['Country', 'Value'])
    df['Country'] = df['Country'].replace(country_mapping)

    # 创建地图
    fig = pxexpress.choropleth(
        df,
        locations='Country',
        locationmode='country names',
        color='Value',
        hover_name='Country',
        hover_data={'Value': True, 'Country': False},
        color_continuous_scale=colorMap,  # 主题
        title=title,
        labels={'Value': '数值'}
    )

    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth',
            scope='world',
            lonaxis_range=[-180, 180],
            lataxis_range=[-90, 90]
        ),
        height=width,
        width=height,
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        font=dict(size=14)
    )

    # 保存为高分辨率 PNG
    fig.write_image("研究国家_地图分布.png", width=width, height=height, scale=scale)
    fig.write_html("研究国家_地图分布.html")
    print("Map saved to world_map.html")
    fig.show()

