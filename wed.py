import re

def load(path : str = 'savedrecs.txt') -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    # 捕获从 PT 开头到 ER（含换行）的一整条记录
    pattern = r"(?=PT )(.*?\nER\n)"
    matches = re.findall(pattern, text, flags=re.DOTALL)

    return matches

# 匹配`SO+一个空格`字符串、`PY+一个空格`字符串
def get_journal_data(entry: str) -> tuple:
    so = re.search(r'^SO (.+)', entry, flags=re.MULTILINE)
    py = re.search(r'^PY\s+(\d{4})', entry, re.MULTILINE)
    return so.group(1).strip() if so else None, py.group(1).strip() if py else None

# 期刊以及发布年份统计，{期刊名字：数量},{年份：数量}
def journal_statistics(items : list[str]):
    sos = {}
    pys = {}
    for item in items:
        so, py = get_journal_data(item)
        if sos.get(so):
            sos[so] += 1
        else:
            sos[so] = 1
        if pys.get(py):
            pys[py] += 1
        else:
            pys[py] = 1
    return sos, pys

# 自定义匹配
def self_define_pattern(entry : str, key : str):
    so = re.search(fr'^{key} (.+)', entry, flags=re.MULTILINE)
    return so.group(1).strip() if so else None

# 自定义统计，键必须和数量有关才行
def self_define_statistics(items : list[str], key : str) -> dict:
    selves = {}
    for item in items:
        rt = self_define_pattern(item, key)
        if selves.get(rt):
            selves[rt] += 1
        else:
            selves[rt] = 1
    return selves

# 对值排序 True表示从大到小
def sort_value(data : dict, reverse : bool = True):
    sorted_data = dict(sorted(data.items(), key=lambda item: item[1], reverse=reverse))
    return sorted_data
# 对键排序
def sort_key(data : dict, reverse : bool = True):
    sorted_data = dict(sorted(data.items(), key=lambda item: int(item[0]), reverse=reverse))
    return sorted_data

# 将每个记录单独写入
def write_record(fileName : str, text : str) -> None:
    with open(fileName, 'w', encoding='U8') as f:
        f.write(text)
        f.close()

def get_cite_count(items : list[str]) -> dict[str, int]:
    rt = {}
    for item in items:
        name = re.search(r'^TI (.+)', item, flags=re.MULTILINE)
        z9_match = re.search(r'^Z9\s+(\d+)', item, flags=re.MULTILINE)
        z9 = int(z9_match.group(1)) if z9_match else 0
        rt[name.group(1).strip()] = z9
    return rt

from collections import OrderedDict
class SliceableDict(OrderedDict):
    def __init__(self, original_dict : dict):
        super().__init__(original_dict)

    def __getitem__(self, key):
        if isinstance(key, slice):
            keys = list(self.keys())[key]
            return SliceableDict({k: self[k] for k in keys})
        else:
            return super().__getitem__(key)

rt = get_cite_count(load())
rt = sort_value(rt, reverse=True)
# print(SliceableDict(rt)[:20])
print((SliceableDict(rt)[:20].keys()))