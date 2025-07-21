from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 学科数据
data = {
    'Energy & Fuels': 557, 'Engineering, Electrical & Electronic': 198, 'Thermodynamics': 165,
    'Green & Sustainable Science & Technology': 135, 'Engineering, Chemical': 103,
    'Environmental Sciences': 41, 'Chemistry, Physical': 41, 'Electrochemistry': 38, 'Mechanics': 36,
    'Computer Science, Information Systems': 33, 'Construction & Building Technology': 25,
    'Telecommunications': 22, 'Environmental Studies': 21, 'Engineering, Multidisciplinary': 20,
    'Engineering, Civil': 18, 'Engineering, Environmental': 17, 'Physics, Applied': 17,
    'Automation & Control Systems': 15, 'Computer Science, Interdisciplinary Applications': 13,
    'Computer Science, Artificial Intelligence': 13, 'Engineering, Mechanical': 12,
    'Materials Science, Multidisciplinary': 11, 'Chemistry, Multidisciplinary': 10,
    'Engineering, Industrial': 10, 'Multidisciplinary Sciences': 9,
    'Operations Research & Management Science': 8, 'Mathematics, Interdisciplinary Applications': 7,
    'Nuclear Science & Technology': 5, 'Computer Science, Cybernetics': 4,
    'Transportation Science & Technology': 3, 'Mathematics': 2, 'Economics': 2,
    'Computer Science, Theory & Methods': 2, 'Nanoscience & Nanotechnology': 2,
    'Engineering, Petroleum': 2, 'Chemistry, Analytical': 1, 'Transportation': 1,
    'Water Resources': 1, 'Mathematics, Applied': 1, 'Ecology': 1, 'Physics, Multidisciplinary': 1,
    'Engineering, Marine': 1, 'Engineering, Ocean': 1, 'Oceanography': 1,
    'Computer Science, Software Engineering': 1, 'Instruments & Instrumentation': 1,
    'Geosciences, Multidisciplinary': 1
}

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 使用浅粉色（冰淇淋色调）作为背景
background_color = "#FFF0F5"  # lavenderblush 也称冰淇淋粉

# 重新生成更密集的词云图
wordcloud = WordCloud(
    width=1600,
    height=900,
    background_color=background_color,
    colormap="Set2",
    prefer_horizontal=0.95,
    margin=1,
    max_font_size=180,         # 增大最大字号
    min_font_size=4,           # 降低最小字号以容纳更多词
    relative_scaling=0.4,      # 控制词频对字体大小的影响程度
    max_words=1000,            # 增加最大词数以生成更密集词云
).generate_from_frequencies(data)

# 显示图像
plt.figure(figsize=(16, 9))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.tight_layout(pad=0)
plt.show()
