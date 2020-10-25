import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import LeaveOneOut


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

def random_split(dateset):
    """随机拆分数据集"""
    train_set,test_set = train_test_split(dateset,test_size=0.2,random_state=42)
    # print(train_set.length,test_set.length)
    return train_set,test_set

def cross_validation(dateset,k=10):
    """K(10)折交叉验证"""
    train_set = []
    test_set = []
    kf = KFold(n_splits=k,shuffle=True,random_state=42)
    for train_index, test_index in kf.split(dateset):
        train_set.append(dateset.iloc[train_index])  # 批量按行提取
        test_set.append(dateset.iloc[test_index])
    return train_set,test_set

def LeaveOne(dateset):
    """留一法"""
    loo = LeaveOneOut()
    train_set = []
    test_set = []
    for train_index,test_index in loo.split(dateset):
        train_set.append(dateset.iloc[train_index])
        test_set.append(dateset.iloc[test_index])
    return train_set,test_set

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




