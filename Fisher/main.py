from LDA import *
from KNN import *
import data_process as dp
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

def main():
    # sonar数据集
    print("Sonar数据集结果：")
    url1 = 'Fisher/Data/sonar/sonar.all-data'
    dateSet = dp.load_dataset(url1)
    dimension_ = 1

    # 交叉验证确定最优k值
    train_seting, test_seting = dp.cross_validation(dateSet, k=10)
    k_best = best_k(train_seting, test_seting, dimension_)    # k_best = 3

    # 随机拆分评估模型
    train_seting_,test_seting_ = dp.random_split(dateSet)
    # 使用sklearn
    X_train, y_train = dp.frame_select(train_seting_)
    X_test, y_test = dp.frame_select(test_seting_)
    lda = LinearDiscriminantAnalysis(n_components=1)
    lda.fit(X_train, y_train)
    x_training, y_training, x_testing, y_testing = lda.transform(X_train), y_train, lda.transform(X_test), y_test

    # 使用自建函数
    # x_training, y_training, x_testing, y_testing = LDA_return(train_seting_, test_seting_, dimension_)
    acc_aa,acc_oa = predict(x_training, y_training, x_testing, y_testing, k_best)
    for i in list(set(y_testing)):
        print("类别%s的预测准确率为: " % i, 100 * acc_aa[i])  # AA
    print("总预测准确率为：{}".format(100 * acc_oa))       # OA

    #iris数据集
    print('\nIris数据集结果：')
    url2 = 'Fisher/Data/iris/iris.data'
    dateset = dp.load_dataset(url2)
    dimension = 2

    # 交叉验证确定k值
    train_set, test_set = dp.cross_validation(dateset, k=10)
    k_best_ = best_k(train_set, test_set, dimension)

    # 随机拆分评估模型
    trainSet,testSet = dp.random_split(dateset)
    x_train, y_train, x_test, y_test = LDA_return(trainSet, testSet, dimension)
    plt.scatter(x_train[:, 0], x_train[:, 1], marker='o', c=y_train)
    plt.show()
    acc_aa,acc_oa = predict(x_train, y_train, x_test, y_test, k_best_)
    for i in list(set(y_test)):
        print("类别%s的预测准确率为: " % i, 100 * acc_aa[i])  # AA
    print("总预测准确率为：{}".format(100 * acc_oa))       # OA

main()