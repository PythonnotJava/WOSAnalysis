import sys, os

from base import merge_large_text_file

"""
# 是什么
- 合并两个WOS文件到一个，放在merge文件夹中
- 使用方法：python空格merge.py空格文件1空格文件2
"""
TARGET = os.path.dirname(os.path.abspath(__file__)) + r'\excel'

def main():
    f1, f2 = sys.argv[1], sys.argv[2]
    merge_large_text_file(f1, f2, f"{TARGET}/merge_out.txt")

if __name__ == '__main__':
    main()