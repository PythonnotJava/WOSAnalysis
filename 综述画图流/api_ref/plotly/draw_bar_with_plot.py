import plotly.graph_objects as go

def draw_bar_with_plot_by_plotly(
    data_bar: dict,
    data_line: Optional[dict] = None,
    xlabel: str = '',
    ylabel: str = '',
    title: str = '',
    bar_color: str = '#457b9d',
    line_color: str = '#e63946',
    **kwargs
):
    keys = list(data_bar.keys())
    bar_values = list(data_bar.values())

    if data_line is None:
        data_line = data_bar
    line_values = [data_line.get(k, 0) for k in keys]

    fig = go.Figure()

    # --- 柱状图 ---
    fig.add_trace(go.Bar(
        x=keys,
        y=bar_values,
        name=ylabel or 'Bar',
        marker_color=bar_color,
        opacity=0.75
    ))

    # --- 折线图（共享y轴） ---
    fig.add_trace(go.Scatter(
        x=keys,
        y=line_values,
        mode='lines+markers',
        name='Trend',
        line=dict(color=line_color, width=3),
        marker=dict(size=8)
    ))

    # --- 美化布局 ---
    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        template='plotly_white',
        legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0)', bordercolor='rgba(0,0,0,0)'),
        **kwargs
    )

    # 可以保存为静态图或 HTML
    # fig.write_image("out/年份变化.png", scale=3)
    # fig.write_html("out/年份变化.html")

    return fig