import sys, os
import pandas, numpy

from base import *

"""
# 是什么
- 如果可视化图并不美观、太难设置配色、只显示部分数据等，gen_excel可以将图源数据导入到excel表格中，表格生成在excel文件夹中，很简单的一键命令、极其无脑。
- 有了数据之后，你就可以直接使用SPSS、Origin等专业可视化软件
- 生成命令：python空格gen_excel.py空格wos记录文件
"""
TARGET = os.path.dirname(os.path.abspath(__file__)) + r'\excel'

def gen_excel_core():
    records = load(sys.argv[1])

    # 年份统计
    years = [match_py(e) for e in records]
    years_data = get_count_single(years)
    year_df = pandas.DataFrame(
        list(years_data.items()),
        columns=["年份", "数量"]
    )
    year_df.to_excel(f'{TARGET}/年份统计.xlsx', index=False)

    # 期刊收录，从高到低
    journals = [match_so(e) for e in records]
    journals_data = get_count_single(journals)
    journals_data = sort_by_value(journals_data, reverse=True)
    journals_data_df = pandas.DataFrame(
        list(journals_data.items()),
        columns=['期刊名字', '数量']
    )
    journals_data_df.to_excel(f'{TARGET}/期刊收录，从高到低.xlsx', index=False)

    # 文章的标题+DOI+综合被引次数，这里有一个想法：如果你有自然语言处理的本事，可以结合AI分析相关性
    title_doi : list[tuple[str, str, int]] = []
    for record in records:
        i = match_z9(record)
        title_doi.append((match_ti(record), match_di(record), i if i else 0))
    title_doi_data = pandas.DataFrame(
        title_doi,
        columns=['标题', 'DOI', '综合被引次数']
    )
    title_doi_data.to_excel(f'{TARGET}/文章的标题+DOI+综合被引次数.xlsx')

    # 匹配学科分类
    subjects = get_count_mult([match_wc(e) for e in records])
    subjects = sort_by_value(subjects, reverse=True)
    subjects_df = pandas.DataFrame(
        list(subjects.items()),
        columns=['学科分类', '数量']
    )
    subjects_df.to_excel(f'{TARGET}/学科分类从高到低统计.xlsx')

    # 匹配研究领域
    researchArea : list[list[str]] = []
    for e in records:
        k = match_sc(e)
        if k:
            researchArea.append(match_sc(e))
    researchArea_data : dict[str, int] = get_count_mult(researchArea)
    researchArea_data = sort_by_value(researchArea_data, reverse=True)
    researchArea_data_df = pandas.DataFrame(
        list(researchArea_data.items()),
        columns=['研究领域', '数量']
    )
    researchArea_data_df.to_excel(f'{TARGET}/研究领域从高到低.xlsx')

    # 出版商
    publisher = [match_pu(r) for r in records]
    publisher_data = get_count_single(publisher)
    publisher_data = sort_by_value(publisher_data, True)
    publisher_data_df = pandas.DataFrame(
        list(publisher_data.items()),
        columns=['出版商', '数量']
    )
    publisher_data_df.to_excel(f'{TARGET}/出版商从高到低统计.xlsx')

    # 附加：综合被引用的从高到低排名的word文件
    reference_with_doi = sort_by_z9_doi(records, True)
    reference_top_with_doi = sort_by_point_value(reference_with_doi, 0)
    gen_word_table(reference_top_with_doi, f'{TARGET}/table_top_all_articles_references')

    print("生成完毕！！！！！！！！！！！！！！！")

if __name__ == '__main__':
    gen_excel_core()

