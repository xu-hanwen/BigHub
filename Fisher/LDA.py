import numpy as np
import data_process as dp
import matplotlib.pyplot as plt

def LDA_main(feature, label, dimension):
    """LDA判别分析算法主体"""
    # 数据按类别整理
    label_ = list(set(label))  # 确定有几类
    X_classify = {}  # 把数据和类对应
    for m in label_:
        X1 = np.array([feature[i] for i in range(len(feature)) if label[i] == m])
        X_classify[m] = X1

    miu = np.mean(feature, axis=0)  # 所有样本的均值
    miu_classify = {}  # 各个样本各自的均值
    for n in label_:
        miu1 = np.mean(X_classify[n], axis=0)
        miu_classify[n] = miu1

    # St = np.dot((X - mju).T, X - mju)
    # 计算类内散度矩阵Sw（总）
    Sw = np.zeros((len(miu), len(miu)))
    for i in label_:
        Sw += np.dot((X_classify[i] - miu_classify[i]).T, X_classify[i] - miu_classify[i])

    # Sb = St-Sw
    # 计算类内散度矩阵Sb
    Sb = np.zeros((len(miu), len(miu)))
    for i in label_:
        Sb += len(X_classify[i]) * np.dot((miu_classify[i] - miu).reshape(
            (len(miu), 1)), (miu_classify[i] - miu).reshape((1, len(miu))))

    # 计算S_w^{-1}S_b的特征值和特征矩阵
    eig_vals, eig_vecs = np.linalg.eig(np.linalg.inv(Sw).dot(Sb))
    eig_vals,eig_vecs = eig_vals.real,eig_vecs.real

    sorted_indices = np.argsort(eig_vals)  # 返回特征值从小到大排序的原索引

    # 提取前k个较大特征向量
    dimension = min(dimension,len(label_)-1)  # k最大为class-1
    topk_eig_vecs = eig_vecs[:, sorted_indices[:-dimension - 1:-1]]
    return topk_eig_vecs

def LDA_return(train_set,test_set,dimension):
    feature, label = dp.frame_select(train_set)
    feature_, label_ = dp.frame_select(test_set)
    w = LDA_main(feature, label, dimension)
    converted_x = np.dot(feature, w)
    converted_test = np.dot(feature_, w)
    return converted_x,label,converted_test,label_

# url = 'Data/sonar/sonar.all-data'
# dateset_ = dp.load_dataset(url)
# dimension_ = 2
# # 随机拆分
# train_set_,test_set_ = dp.random_split(dateset_)
# X_train_,y_train_,X_test_,y_test_ = LDA_return(train_set_, test_set_, dimension_)
