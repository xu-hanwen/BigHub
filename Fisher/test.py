import numpy as np
import data_process as dp
from KNN import *
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


def best_k(train_set,test_set):
    k_range = range(1, 21, 2)
    k_acc = []
    for k in k_range:
        acc = 0
        for i in range(0, 10):
            X, y = dp.frame_select(train_set[i])
            X_, y_ = dp.frame_select(test_set[i])
            lda = LinearDiscriminantAnalysis(n_components=1)
            lda.fit(X, y)
            X_train, Y_train, X_test, Y_test = lda.transform(X), y, lda.transform(X_), y_
            _, acc_oa = predict(X_train, Y_train, X_test, Y_test, k)
            acc += acc_oa
        k_acc.append(acc / 10)

    plt.plot(k_range, k_acc)
    plt.xlabel('value of k for knn')
    plt.ylabel('cross-validated Accuracy')
    plt.show()
    # 求出最佳k值
    index_max = k_acc.index(max(k_acc))
    k_best = list(k_range)[index_max]
    print('KNN中最佳k值为：', k_best)
    return k_best

def main():
    # Sonar数据集
    url = 'Data/sonar/sonar.all-data'
    dateset = dp.load_dataset(url)
    dimension_ = 2

    train_set, test_set = dp.cross_validation(dateset, k=10)
    k_best = best_k(train_set,test_set)

    train_seting_, test_seting_ = dp.random_split(dateset)
    X,y = dp.frame_select(train_seting_)
    X_,y_ = dp.frame_select(test_seting_)
    lda = LinearDiscriminantAnalysis(n_components=1)
    lda.fit(X, y)
    x_training, y_training, x_testing, y_testing = lda.transform(X),y,lda.transform(X_),y_
    acc_aa, acc_oa = predict(x_training, y_training, x_testing, y_testing, k_best)
    for i in list(set(y_testing)):
        print("类别%s的预测准确率为: " % i, 100 * acc_aa[i])  # AA
    print("总预测准确率为：{}".format(100 * acc_oa))  # OA

    # Iris数据集
    url = 'Data/iris/iris.data'
    dateset = dp.load_dataset(url)
    X, y = dp.frame_select(dateset)
    lda = LinearDiscriminantAnalysis(n_components=2)
    lda.fit(X, y)
    X_new = lda.transform(X)
    print(X_new.shape)
    # print('Coefficients:%s, intercept %s' % (lda.coef_, lda.intercept_))  # w和b
    plt.scatter(X_new[:, 0], X_new[:, 1], marker='o', c=y)
    plt.show()


main()
