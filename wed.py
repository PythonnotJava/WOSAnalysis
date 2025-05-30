"""
文章的标题，我想使用自然语言工具根据语义找出他们的共性进行聚类，然后对每个聚类都分配一个概述标签
"""

import re
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import numpy as np
from collections import defaultdict

def load(path : str = 'savedrecs.txt') -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    # 捕获从 PT 开头到 ER（含换行）的一整条记录
    pattern = r"(?=PT )(.*?\nER\n)"
    matches = re.findall(pattern, text, flags=re.DOTALL)

    return matches

def self_define_pattern(entry : str, key : str):
    so = re.search(fr'^{key} (.+)', entry, flags=re.MULTILINE)
    return so.group(1).strip() if so else None

titles = []

for item in load():
    titles.append(self_define_pattern(item, 'TI'))

# print(titles)

# 示例标题
titles = titles

# 1. 生成语义嵌入
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(titles)

# 2. 聚类（你可以改为 HDBSCAN 更自动）
num_clusters = 3
clustering_model = KMeans(n_clusters=num_clusters, random_state=42)
clustering_labels = clustering_model.fit_predict(embeddings)

# 3. 分组标题
clustered_titles = defaultdict(list)
for title, label in zip(titles, clustering_labels):
    clustered_titles[label].append(title)

# 4. 为每个聚类生成标签（取最接近中心的标题）
def get_cluster_label(cluster_id, indices, embeddings, titles):
    center = clustering_model.cluster_centers_[cluster_id]
    cluster_embeddings = embeddings[indices]
    distances = np.linalg.norm(cluster_embeddings - center, axis=1)
    closest_idx = indices[np.argmin(distances)]
    return titles[closest_idx]

# 5. 打印结果
with open('output.txt', 'w', encoding='u8') as file:
    for cluster_id, titles_in_cluster in clustered_titles.items():
        indices = [i for i, label in enumerate(clustering_labels) if label == cluster_id]
        label = get_cluster_label(cluster_id, indices, embeddings, titles)
        print(f"Cluster {cluster_id} - Label: {label}")
        file.write(f'Cluster {cluster_id} - Label: {label}')
        for title in titles_in_cluster:
            print(f"  - {title}")
            file.write(title)
        print()
    file.close()
print('Done')