import re, os, platform, shutil
from typing import Optional
from collections import OrderedDict

from docx import Document

# 可切片字典
class SliceableDict(OrderedDict):
    def __init__(self, original_dict : dict):
        super().__init__(original_dict)

    def __getitem__(self, key):
        if isinstance(key, slice):
            keys = list(self.keys())[key]
            return SliceableDict({k: self[k] for k in keys})
        else:
            return super().__getitem__(key)

# 桌面路径
def get_desktop_path():
    system = platform.system()
    if system == "Windows":
        return os.path.join(os.environ['USERPROFILE'], 'Desktop')
    elif system == "Darwin":  # macOS
        return os.path.join(os.path.expanduser("~"), "Desktop")
    else:  # Linux
        return os.path.join(os.path.expanduser("~"), "桌面")  # 有些Linux中文系统桌面文件夹叫“桌面”

# 匹配记录到列表
def load(path : str = 'savedrecs.txt') -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    # 捕获从 PT 开头到 ER（含换行）的一整条记录
    pattern = r"(?=PT )(.*?\nER\n)"
    matches = re.findall(pattern, text, flags=re.DOTALL)

    return matches

# 快速合并两个大纯文本文件
def merge_large_text_file(file1: str, file2: str, output: str) -> None:
    with open(output, 'wb') as fout:
        with open(file1, 'rb') as f1:
            shutil.copyfileobj(f1, fout)
        fout.write(b'\n')
        with open(file2, 'rb') as f2:
            # 跳过前 skip_lines 行
            for _ in range(2):
                f2.readline()
            shutil.copyfileobj(f2, fout)

# 退出App清空记录
def clearRecords() -> None:
    for file in os.listdir('records'):
        file_path = os.path.join('records', file)
        os.remove(file_path)

# 按照值排序，reverse为True从大到小
def sort_by_value(data : dict, reverse=False):
    return dict(sorted(data.items(), key=lambda item: item[1], reverse=reverse))

# 按照键排序，reverse为True从大到小
def sort_by_key(data : dict, reverse=False):
    return dict(sorted(data.items(), key=lambda item: item[0], reverse=reverse))

# 匹配发表年份
def match_py(entry : str) -> Optional[str]:
    py = re.search(r'^PY\s+(\d{4})', entry, re.MULTILINE)
    return py.group(1).strip() if py else None

# 匹配期刊名称
def match_so(entry : str) -> Optional[str]:
    so = re.search(r'^SO (.+)', entry, flags=re.MULTILINE)
    return so.group(1).strip() if so else None

# 匹配文章标题，标题是必有的
# 匹配从 TI 到 SO 之间的所有内容，跨越多行
def match_ti(entry : str) -> str:
    pattern = r"TI\s+(.+?)(?=\nSO)"
    match = re.search(pattern, entry, flags=re.DOTALL)
    title = match.group(1).strip()
    title = title.replace("\n   ", " ")  # 将标题中的换行符替换为空格
    return title

# 匹配综合被引次数
def match_z9(entry : str) -> Optional[int]:
    pattern = r"Z9\s+(\d+)"
    match = re.search(pattern, entry)
    if match:
        return int(match.group(1))
    return None

# 匹配学科分类
def match_wc(entry : str) -> Optional[list[str]]:
    lines = entry.splitlines()
    wc_lines = []
    in_wc = False
    for line in lines:
        if in_wc:
            # 遇到新字段（两大写字母+空格开头且非WC）停止
            if re.match(r"^[A-Z]{2} ", line) and not line.startswith("WC "):
                break
            # 缩进行或者空白行认为是WC续行
            if line.startswith(' ') or line.startswith('\t') or line.strip() == '':
                wc_lines.append(line.strip())
            else:
                # 碰到非缩进非字段的行，也加入，防止遗漏
                wc_lines.append(line.strip())
        else:
            if line.startswith("WC "):
                in_wc = True
                # 去除"WC "开头
                wc_lines.append(line[3:].strip())
    if not wc_lines:
        return None
    # 合并所有行，用空格替代换行
    wc_text = ' '.join(wc_lines)
    # 分号切分，去除两端空白
    categories = [c.strip() for c in wc_text.split(';')]
    return categories

# 匹配研究领域，这个很短，没有多行情况，即使有，不差这一两个被忽略
def match_sc(entry : str) -> Optional[list[str]]:
    pattern = r"^SC\s+(.+)$"
    match = re.search(pattern, entry, flags=re.MULTILINE)
    if match:
        text = match.group(1).strip()
        categories = [c.strip() for c in text.split(';')]
        return categories
    return None

# 匹配出版商，只考虑唯一性
def match_pu(entry : str) -> Optional[str]:
    pattern = r"^PU\s+(.+)$"
    match = re.search(pattern, entry, flags=re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None

# 对于单个值返回进行统计，适用于年份、出版商等情况
def get_count_single(target : list[str]) -> dict[str, int]:
    result = {}
    for key in target:
        if result.get(key):
            result[key] += 1
        else:
            result[key] = 1
    return result

# 对于返回的列表系列进行统计，适用于学科分类、研究领域等情况
def get_count_mult(target : list[list[str]]) -> dict[str, int]:
    result = {}
    for innerList in target:
        for item in innerList:
            if result.get(item):
                result[item] += 1
            else:
                result[item] = 1
    return result

# 根据引用次数对论文排序，默认从大到小
def sort_by_z9(records : list[str], reverse=True) -> dict[str, int]:
    result = {}
    for entry in records:
        z9 = match_z9(entry)
        ti = match_ti(entry)
        if z9 is not None and ti is not None : # 不要直接if name，因为引用数目可能为0
            result[ti] = z9
        else:
            print(ti)
    return sort_by_value(result, reverse)

# 匹配文章的DOI，一定有
def match_di(entry : str) -> str:
    match = re.search(r'^DI (.+)', entry, flags=re.MULTILINE)
    return match.group(1).strip()

# 根据引用次数对论文排序，默认从大到小，同时附加DOI
def sort_by_z9_doi(records : list[str], reverse=True) -> dict[str, tuple[int, str]]:
    result = {}
    for entry in records:
        z9 = match_z9(entry)
        ti = match_ti(entry)
        doi = match_di(entry)
        if z9 is not None and ti is not None and doi is not None: # 不要直接if name，因为引用数目可能为0
            result[ti] = (z9, doi)
    return sort_by_value(result, reverse)

# 根据一个键有多个值的某个值大小排序
# 比如说{'A' : [32, 23], 'B' : [12, 0]}
def sort_by_point_value(data : dict, which : int, reverse=True):
    return dict(sorted(data.items(), key=lambda item: item[1][which], reverse=reverse))

# 生成文章引用排序的markdown表格
def gen_md_table_by_reference(articles : dict[str, tuple[int, str]]) -> str:
    headers = '|Article Name|DOI|Citations|\n|--|--|--|\n'
    for name, (ca, doi) in articles.items():
        headers += f'|{name}|{doi}|{ca}|\n'
    return headers

# md表格生成word表格
def gen_word_table(articles : dict[str, tuple[int, str]], output : str) -> None:
    doc = Document()
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'

    # 设置表头
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Article Name'
    hdr_cells[1].text = 'DOI'
    hdr_cells[2].text = 'Citations'
    # 添加数据行
    for name, (citations, doi) in articles.items():
        row_cells = table.add_row().cells
        row_cells[0].text = name
        row_cells[1].text = doi
        row_cells[2].text = str(citations)

    doc.save(f'{output}.docx')