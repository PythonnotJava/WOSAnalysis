# 基于WOS导出文献完整记录做数据可视化分析

说明：WOS导出的每一项文献都是以PT开始并且以ER结尾，我称之为一栏。

下面是对于标记的信息映射表说明。

| 标记   | 信息说明                  |
|------|-----------------------|
| PT   | 文献类型（J = 期刊文章）        |
| AU   | 作者（缩写形式）              |
| AF   | 作者全名                  |
| TI   | 文章标题                  |
| SO   | 期刊名                   |
| LA   | 语言                    |
| DT   | 文献类型描述（如 Article）     |
| DE   | 作者关键词                 |
| AB   | 摘要                    |
| C1   | 作者单位及地址               |
| RP   | 通讯作者及地址               |
| EM   | 作者邮箱                  |
| RI   | ResearcherID          |
| OI   | ORCID 标识符             |
| FU   | 资助机构                  |
| FX   | 资助声明（Funding Text）    |
| NR   | 参考文献数                 |
| TC   | 被引用次数（Times Cited）    |
| Z9   | 综合被引次数                |
| U1   | 使用次数（近 180 天）         |
| U2   | 使用次数（自 2013 年起）       |
| PU   | 出版商                   |
| PI   | 出版地                   |
| PA   | 出版商地址                 |
| EI   | 电子 ISSN               |
| J9   | 来源期刊缩写                |
| JI   | 来源期刊简称                |
| PD   | 发表月份                  |
| PY   | 发表年份                  |
| VL   | 卷号（Volume）            |
| IS   | 期号（Issue）             |
| AR   | 文章编号（Article Number）  |
| DI   | DOI（数字对象标识符）          |
| PG   | 页数                    |
| WC   | Web of Science 分类（学科） |
| WE   | Web of Science 索引库    |
| SC   | 学科类别                  |
| GA   | 文献标识号（WOS 内部用）        |
| UT   | Web of Science 唯一标识码  |
| OA   | 开放获取类型（如 gold）        |
| DA   | 数据导出日期                |
| ER   | 记录结束标志                |


## 特点说明
- 该程序是可拓展的，比如说可视化方面添加一个气泡图分析，又或者分析方面添加文献类型（DT字段），甚至你可以设置别的数据库的导出格式
- 功能核心是多线程的，可以轻松拓展新功能到新线程
- 最简单的方法就是：去改[core.py](core.py)里面的get_journal_data的正则表达式

## Example
![src](example/1.jpg)
![src](example/2.png)
![src](example/3.png)
![src](example/4.png)

> 在大量（如下图，200+期刊源，柱状图表现很差，于是需要词云或者其他图显示）
> 
![src](example/5.png)

## 依赖
```text
Python >= 3.12
pyside6
matplotlib
wordcloud
qtawesome

```