import pandas as pd
from sklearn.preprocessing import LabelEncoder

def load_dataset(url):
    """数据集加载"""
    dateset= pd.read_csv(url,header=None)
    # 数据分析
    # print(dateset.head())   # 查看前五行数据
    # print(dateset.info())   # 获取数据集的简单描述
    # print(dateset['class'].value_counts())  # 分类信息
    # print(dateset.describe())   # 每个数值属性摘要
    # dateset.hist(bins=30,figsize=(10,8))  # 绘制每个数值属性的直方图
    return dateset

def frame_select(date):
    """属性拆分与处理(转换为NumPy数组)"""
    feature = date.drop([date.columns[-1]],axis=1).values
    label = date.iloc[:,-1].values
    # 数值编码
    encoder = LabelEncoder()
    label_ = encoder.fit_transform(label)
    return feature,label_

# url = 'Data/iris/iris.data'
# dataset = load_dataset(url)
# frame_select(dataset)




