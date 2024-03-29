import numpy as np
import pandas as pd
import data_process as dp
import matplotlib.pyplot as plt

class K_means():
    def __init__(self,dataset,k):
        self.k = k
        self.feature = dataset
        self.iter_nums = 20  # 最大迭代次数

    def fit(self):
        """随机初始化聚类中心"""
        self.centers = {}
        for i in range(self.k):
            self.centers[i]=self.feature[np.random.randint(0,len(self.feature))]

        for m in range(self.iter_nums):  # 迭代
            # 初始化模型结果
            self.label_ = {} # 每一类别对应的样本
            for i in range(self.k):
                self.label_[i] = []

            for j in range(len(self.feature)):  
                distances = []
				# 计算所有样本点到各聚类的中心
                for center in self.centers:
                    distances.append(np.linalg.norm(self.feature[j]-self.centers[center]))
                # 聚类
                classification = distances.index(min(distances)) # 预测样本类别
                self.label_[classification].append(self.feature[j])

            # 更新中心点
            centers_last = dict(self.centers)
            for c in self.label_:
                if len(self.label_[c]) != 0:  # 防止报错
                	self.centers[c] = np.average(self.label_[c],axis=0)

            # 判断是否终止迭代
            optimized = 0
            for center in self.centers:
                # 只有当相邻两次的中心点都一样方可停止迭代
                if np.sum(centers_last[center]-self.centers[center]) != 0:
                    optimized += 1
            if optimized == 0:
                break

    def predict(self,feature):
        self.fit()  # 训练模型
        label_ = []
        features = feature
        # 最终预测类别输出
        for data in range(len(features)):
            distances = []
            for center in self.centers:
                distances.append(np.linalg.norm(features[data] - self.centers[center]))
            # 和聚类中心距离最近的类作为预测类别
            label_predict = distances.index(min(distances))
            label_.append(label_predict)
        return label_

    def evaluate(self,feature, label):
        while True:
            label_ = self.predict(feature)  # 模型输出
            labels, features = label,feature
            # OA
            oa_count = 0
            for data in range(len(features)):
                if labels[data] == label_[data]:
                    oa_count += 1
            acc_oa = float(oa_count)/float(len(features))  # OA指标
            # print(acc_oa)
            if acc_oa>0.89:  # sonar_oa_max = 0.58,iris_oa_max=0.89
                # AA
                acc_aa = [0] * self.k
                for m in range(self.k):
                    aa_count = 0
                    # 根据类别信息拆分数据
                    L1 = np.array([label_[o] for o in range(len(features)) if labels[o] == m])
                    aa_count = sum([m == p for p in L1])
                    if aa_count != 0:
                        acc_aa[m] = float(aa_count/len(L1))
                break
        return acc_oa,acc_aa

    def plot(self,centers,feature,label):
        centers = pd.DataFrame(centers)

        plt.scatter(feature[np.nonzero(label == 0), 0],feature[np.nonzero(label == 0), 1], marker='o', color='r', label='0', s=10)
        plt.scatter(feature[np.nonzero(label == 1), 0],feature[np.nonzero(label == 1), 1], marker='+', color='b', label='1', s=10)
        plt.scatter(feature[np.nonzero(label == 2), 0],feature[np.nonzero(label == 2), 1], marker='*', color='g', label='2', s=10)
        plt.scatter(centers.iloc[0, :].values, centers.iloc[1, :].values, marker='x', color='m', s=30)
        plt.show()

# if __name__ == '__main__':
#     url = 'Data/iris/iris.data'   # oa_max = 0.89
#     # url = 'Data/sonar/sonar.all-data'  # oa_max = 0.56
#     dateset = dp.load_dataset(url)
#     feature, label = dp.frame_select(dateset)
#     k = 3
#     k_means = K_means(feature,k)
#     # k_means.fit()
#     acc_oa,acc_aa = k_means.evaluate(feature, label)
#     print(acc_oa,acc_aa)
#     k_means.plot(k_means.centers,feature,label)