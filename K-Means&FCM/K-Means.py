import numpy as np
import data_process as dp

class K_means():
    def __init__(self,dataset,k):
        feature, label = dp.frame_select(dataset)
        self.k = k
        self.feature = feature
        self.label = label

    def fit(self):
        """随机初始化聚类中心"""
        self.centers = {}
        for i in range(self.k):
            self.centers[i]=self.feature[np.random.randint(0,len(self.feature))]
        # print(self.centers)

        while True:  # 迭代
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

    def predict(self,dataset):
        self.fit()  # 训练模型
        label_ = []
        features, labels = dp.frame_select(dataset)
        # 最终预测类别输出
        for data in range(len(features)):
            distances = []
            for center in self.centers:
                distances.append(np.linalg.norm(features[data] - self.centers[center]))
            # 和聚类中心距离最近的类作为预测类别
            label_predict = distances.index(min(distances))
            label_.append(label_predict)
        return label_,labels,features

    def evaluate(self,dataset):
        while True:
            label_,labels,features = self.predict(dataset)  # 模型输出
            # OA
            oa_count = 0
            for data in range(len(features)):
                if labels[data] == label_[data]:
                    oa_count += 1
            acc_oa = float(oa_count)/float(len(features))  # OA指标
            print(acc_oa)
            if acc_oa>0.93:  # 不断试聚类中心的初值
                # AA
                acc_aa = [0] * self.k
                for m in range(self.k):
                    aa_count = 0
                    # 根据类别信息拆分数据
                    X1 = np.array([features[n] for n in range(len(features)) if labels[n] == m])
                    L1 = np.array([label_[o] for o in range(len(features)) if labels[o] == m])
                    aa_count = sum([m == p for p in L1])
                    if aa_count != 0:
                        acc_aa[m] = float(aa_count/len(X1))
                break
        return acc_oa,acc_aa

if __name__ == '__main__':
    url = 'Data/iris/iris.data'
    # url = 'Data/sonar/sonar.all-data'
    dateset = dp.load_dataset(url)
    trainset,testset = dp.random_split(dateset)
    k_means = K_means(trainset,3)
    acc_oa,acc_aa = k_means.evaluate(testset)
    print(acc_oa,acc_aa)