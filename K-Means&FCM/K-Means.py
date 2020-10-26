import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold


def load_data(url):
    dataset = pd.read_csv(url,header=None)
    # 随机拆分数据集
    train_set, test_set = train_test_split(dataset, test_size=0.3, random_state=42)
    # print(train_set.length,test_set.length)
    return train_set, test_set

def frame_select(date):
    """属性拆分与处理(转换为NumPy数组)"""
    feature = date.drop([date.columns[-1]],axis=1).values
    label = date.iloc[:,-1].values
    # 数值编码
    encoder = LabelEncoder()
    label = encoder.fit_transform(label)
    return feature,label

class K_means():
    def __init__(self,trainset,k):
        feature, label = frame_select(trainset)
        self.k = k
        self.feature = feature
        self.label = label

    def fit(self):
        # 随机初始化各类中心
        self.centers = {}
        for i in range(self.k):
            self.centers[i]=self.feature[i]

        while True:  # 迭代
            # 初始化模型结果
            self.label_ = {}
            for i in range(self.k):
                self.label_[i] = []

            for j in range(len(self.feature)):  # 拿出每个样本
                distances = []
                for center in self.centers:
                    distances.append(np.linalg.norm(self.feature[j]-self.centers[center]))
                classification = distances.index(min(distances))
                self.label_[classification].append(self.feature[j])

            # 更新中心点
            centers_last = dict(self.centers)
            for c in self.label_:
                self.centers[c] = np.average(self.label_[c],axis=0)

            # 判断是否终止迭代
            optimized = 0
            for center in self.centers:
                if np.sum(centers_last[center]-self.centers[center]) != 0:
                    optimized += 1
            if optimized == 0:
                break

    def predict(self,dataset):
        oa_count = 0
        acc_aa = [0] * self.k

        feature, label = frame_select(dataset)
        for data in range(len(feature)):
            distances = []
            for center in self.centers:
                distances.append(np.linalg.norm(feature[data] - self.centers[center]))
            label_predict = distances.index(min(distances))
            if label[data] == label_predict:
                oa_count += 1
        acc_oa = float(oa_count)/float(len(feature))  # OA指标

        for i in range(self.k):
            aa_count = 0
            X1 = np.array([feature[j] for j in range(len(feature)) if label[j] == i])
            X1_ = np.array([label[j] for j in range(len(feature)) if label[j] == i])
            for data in range(len(X1)):
                distances = []
                for center in self.centers:
                    distances.append(np.linalg.norm(X1[data] - self.centers[center]))
                label_predict = distances.index(min(distances))
                if X1_[data] == label_predict:
                    aa_count += 1
            acc_aa[i] = float(aa_count) / float(len(X1))  # OA指标
        return acc_oa,acc_aa

if __name__ == '__main__':
    # url = 'Data/iris/iris.data'
    url = 'Data/sonar/sonar.all-data'
    train_set, test_set = load_data(url)
    k_means = K_means(train_set,2)
    k_means.fit()
    acc_oa,acc_aa = k_means.predict(train_set)
    print(acc_oa,acc_aa)








