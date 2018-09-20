import pandas as pd
import numpy as np
import jenkspy
import math


# values:数据列表  classes:分类数  mode：模式
def get_split_point(values, classes, mode, result_decimal):
    rets = []

    if mode == 'equal_count':  # 等宽
        df = pd.DataFrame(np.array(values), columns=['data'])
        for i in range(classes):
            p = (i + 1) / classes
            rets.append(df.quantile(p, 0, 'linear')['data'])

    elif mode == 'equal_interval':  # 等间隔
        value_interval = (max(values) - min(values)) / classes
        for i in range(classes):
            rets.append(min(values) + value_interval * (i + 1))

    elif mode == 'nature_breaks':  # 自然裂点
        rets = jenkspy.jenks_breaks(values, classes)
        rets.pop(0)

    elif mode == 'standard_deviation':  # 标准差
        avg_value = sum(values) / len(values)
        p = pd.Series(values).std()
        delta = (math.ceil(classes / 2) - 1) * 0.5
        for i in range(classes - 1):
            rets.append(avg_value + p * (i * 0.5 - delta))
        rets.append(max(values))

    return [round(x, int(result_decimal)) for x in rets]

