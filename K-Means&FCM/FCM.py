import numpy as np
import pandas as pd
import data_process as dp
import matplotlib.pyplot as plt
# from Fisher.LDA import LDA_return
import random

class FCM():
    def __init__(self,k,dataset,alpha):
        self.features,self.lables = dp.frame_select(dataset)
        self.k = k
        self.num_features = len(self.features)
        self.alpha = alpha

    # 初始化模糊矩阵U
    def initial_Matrix_U(self):
        self.mat_U = []
        for i in range(self.num_features):
            random_num_list = [np.random.random() for i in range(self.k)]
            # 归一化
            sum_list = sum(random_num_list)
            temp_list = [x / sum_list for x in random_num_list]
            self.mat_U.append(temp_list)
        print(self.mat_U[0])

    # 计算类中心点
    # Zj = (i=1,i=n){∑(Uij)^(alpha)*Xi}/(i=1,i=n){∑(Uij)^alpha}
    def Class_center(self):
        self.mat_U = np.array(self.mat_U)  # n*k
        self.class_centers = list()
        for j in range(self.k):
            x = self.mat_U[:,j]
            U_alpha = [e ** self.alpha for e in x]
            sum_u_alpha = sum(U_alpha)  # 分母
            temp_num = list()
            Uj_alpha_xi = sum(U_alpha[i] * self.features[i] for i in range(self.num_features))  # 分子
            center = [z / sum_u_alpha for z in Uj_alpha_xi]
            self.class_centers.append(center)
        # return class_centers

    # 更新隶属矩阵
    # 1/(k=1,k=c){∑(dij /dik)^[2/(alpha-1)]}
    def update_Matrix_U(self):
        data = []
        for i in range(self.num_features):
            x = self.features[i] # 取出文件中的每一行数据
            distances = [np.linalg.norm(x-self.class_centers[k]) for k in range(self.k)]  # [dik]
            for j in range(self.k):
                den = sum([np.power(float(distances[j] / distances[c]), float(2/(self.alpha-1))) for c in range(self.k)])
                self.mat_U[i][j] = float(1 / den)

    # 得到聚类结果
    def get_lables(self):
        lables_ = list()
        for i in range(self.num_features):
            max_val, idx = max((val, idx) for (idx, val) in enumerate(self.mat_U[i]))
            lables_.append(idx)
        return lables_

    # 计算代价函数
    # J = (j=1,j=c)∑Jj
    # Jj = (i=1,j=m)∑[(Uij)^(alpha) * dij^2]
    def J_function(self):
        J = 0
        for j in range(self.k):
            x = self.mat_U[:,j]
            U_alpha = [e ** self.alpha for e in x]
            temp_num = list()
            for i in range(self.num_features):
                distances = np.power(np.linalg.norm(self.features[i] - self.class_centers[j]), 2)  # dij^2
                prod = U_alpha[i] * distances
                temp_num.append(prod)  # Uij^(alpha)*dij^2
            Jj = np.sum(temp_num)
            J += Jj
        return J

    def predict(self):
        # 预测主程序
        self.initial_Matrix_U()
        J_last = 0
        while True:  # 最大迭代次数
            self.Class_center()  # 计算聚类中心点
            J = self.J_function()   # 计算代价函数
            # print(J)
            # 判断终止条件
            if J_last == J:
                break
            J_last = J
            self.update_Matrix_U()  # 更新隶属度矩阵
        lables_ = self.get_lables()  # 求预测类别
        return lables_

    def evaluate(self):
        while True:
            lables_ = self.predict()
            # OA
            total_num = 0
            for i in range(self.num_features):
                if self.lables[i] == lables_[i]:
                    total_num += 1
            acc_oa = float(total_num/self.num_features)
            if acc_oa > 0.8:
                break
            # AA
            # acc_aa = [0] * self.k
            # for j in range(self.k):
            #     aa_count = 0
            #     L1_ ,X1= [],[]
            #     for i in range(self.num_features):
            #         if self.lables[i] == j:
            #             X1.append(self.features[i])
            #             L1_.append(lables_[i])
            #     for data in range(len(X1)):
            #         if j == L1_[data]:
            #             aa_count += 1
            #     acc_aa[j] = float(aa_count) / float(len(X1))  # OA指标
        return acc_oa

if __name__ == '__main__':
    # random.seed(10)
    # url = 'Data/iris/iris.data'
    url = 'Data/sonar/sonar.all-data'
    dataset = dp.load_dataset(url)
    trainset, testset = dp.random_split(dataset)
    # 进行LDA降维
    # dimension = 2
    # X_train, y_train, X_test, y_test = LDA_return(trainset, testset, dimension)
    # FCM聚类
    k = 3
    alpha = 1.5
    Fcm = FCM(k,trainset,alpha)

    acc_oa = Fcm.evaluate()
    center_array = np.array(Fcm.class_centers)
    print(acc_oa)

    # 做散点图
    plt.scatter(Fcm.features[np.nonzero(Fcm.lables == 0), 0], Fcm.features[np.nonzero(Fcm.lables == 0), 1], marker='o', color='r', label='0', s=10)
    plt.scatter(Fcm.features[np.nonzero(Fcm.lables == 1), 0], Fcm.features[np.nonzero(Fcm.lables == 1), 1], marker='+', color='b', label='1', s=10)
    plt.scatter(Fcm.features[np.nonzero(Fcm.lables == 2), 0], Fcm.features[np.nonzero(Fcm.lables == 2), 1], marker='*', color='g', label='2', s=10)
    plt.scatter(center_array[:, 0], center_array[:, 1], marker='x', color='m', s=30)
    plt.show()
