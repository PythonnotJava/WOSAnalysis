import pandas

from draw_map import drawMapByDefine


def readDataFrame(file: str = 'src/savedrecs.xls'):
    dataFrames: pandas.DataFrame = pandas.read_excel(file)
    return dataFrames


def getHistCount[T](datas: list[T]) -> dict[T, int]:
    result: dict[T, int] = {}
    for data in datas:
        result.update({data: result.get(data, 0) + 1})
    return result


def getRuleCount(datas: dict[str, int]) -> None:
    for k, v in list(datas.items()):
        if 'USA' in k and k != 'USA':
            datas['USA'] = datas.get('USA', 0) + v
            datas.pop(k)
        elif k == 'Peoples R China' or k == 'PRC':
            datas['China'] = datas.get('China', 0) + v
            datas.pop(k)
        elif k == 'Turkiye':
            datas['Turkey'] = datas['Turkey'] + v
            datas.pop(k)
        elif k == 'Scotland' or k == 'Wales':
            datas['England'] += datas['England'] + v
            datas.pop(k)
        elif k == 'Taiwan':
            datas['China'] = datas.get('China', 0) + v
            datas.pop(k)
    return

def getCountryToList(dataFrames: pandas.DataFrame):
    q: list[str] = []
    for data in dataFrames['Addresses']:
        if not pandas.isna(data):
            q.append(data.split(', ')[-1])

    return q


def getCopedCountryMap(datas: list[str]) -> dict[str, int]:
    countryMaps = getHistCount(datas)
    getRuleCount(countryMaps)
    return countryMaps


if __name__ == '__main__':
    datas = getCopedCountryMap(
            getCountryToList(
                readDataFrame()
            )
        )
    print(datas)
    drawMapByDefine(
        datas
    )
