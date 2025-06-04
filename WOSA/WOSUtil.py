import re, os, platform
from collections import OrderedDict

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

def load(path : str = 'savedrecs.txt') -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    # 捕获从 PT 开头到 ER（含换行）的一整条记录
    pattern = r"(?=PT )(.*?\nER\n)"
    matches = re.findall(pattern, text, flags=re.DOTALL)

    return matches

