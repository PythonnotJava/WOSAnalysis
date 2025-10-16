import random

# 深色为主
def deep_main(*args, **kwargs):
    # 候选深色
    colors = [
        "#2e2e6f",  # 深蓝
        "#000080",  # 藏青
        "#4b0082",  # 靛蓝
        "#301934",  # 深紫
        "#191970",  # 午夜蓝
        "#2c003e" ,
        "#8dda91",
        "#fbeb4e",
        "#2e6e8e"
    ]
    return random.choice(colors)