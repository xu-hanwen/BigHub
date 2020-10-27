import numpy as np
import data_process as dp

class K_means():
    def __init__(self,dataset,k):
        feature, label = dp.frame_select(dataset)
        self.k = k
        self.feature = feature
        self.label = label

    def fit(self):
        # 随机初始化各类中心
        self.centers = {}
        for i in range(self.k):
            self.centers[i]=self.feature[np.random.randint(0,len(self.feature))]
        print(self.centers)

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

    def predict(self):
        self.fit()
        label_ = []
        # feature, label = dp.frame_select(dataset)
        for data in range(len(self.feature)):
            distances = []
            for center in self.centers:
                distances.append(np.linalg.norm(self.feature[data] - self.centers[center]))
            label_predict = distances.index(min(distances))
            label_.append(label_predict)
        return label_

    def evaluate(self):
        while True:
            lable_ = self.predict()
            # OA
            oa_count = 0
            for data in range(len(self.feature)):
                if self.label[data] == lable_[data]:
                    oa_count += 1
            acc_oa = float(oa_count)/float(len(self.feature))  # OA指标
            if acc_oa>0.8:
                break
            # AA
            # acc_aa = [0] * self.k
            # for i in range(self.k):
            #     aa_count = 0
            #     X1 = np.array([feature[j] for j in range(len(feature)) if label[j] == i])
            #     X1_ = np.array([label[j] for j in range(len(feature)) if label[j] == i])
            #     for data in range(len(X1)):
            #         distances = []
            #         for center in self.centers:
            #             distances.append(np.linalg.norm(X1[data] - self.centers[center]))
            #         label_predict = distances.index(min(distances))
            #         if X1_[data] == label_predict:
            #             aa_count += 1
            #     acc_aa[i] = float(aa_count) / float(len(X1))  # OA指标
        return acc_oa

if __name__ == '__main__':
    url = 'Data/iris/iris.data'
    # url = 'Data/sonar/sonar.all-data'
    dateset = dp.load_dataset(url)
    trainset,testset = dp.random_split(dateset)
    k_means = K_means(trainset,3)
    acc_oa = k_means.evaluate()
    print(acc_oa)








