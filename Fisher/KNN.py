from LDA import *
import numpy as np

#knn算法
def knn(trainSet,label,testSet,k):
    # 计算欧式距离
    distance=(trainSet-testSet)**2  # 求差的平方和
    # 对数组的每一行求和
    distanceLine=distance.sum(axis=1)
    finalDistance=distanceLine**0.5

    # 对距离进行排序
    sortedIndex=finalDistance.argsort()    # 获得排序后原始下角标
    # 获得距离最小的前k个下角标
    index=sortedIndex[:k]
    # 字典 key为标签，value为标签出现的次数
    labelCount={}
    for i in index:
        tempLabel=label[i]
        # 对选取的k个样本所属类别个数进行统计
        labelCount[tempLabel]=labelCount.get(tempLabel,0)+1
    maxCount = 0
    for key, value in labelCount.items():
        if value > maxCount:
            maxCount = value
            classes = key
    return classes

#预测正确率
def predict(trainSet,trainLabel,testSet,testLabel,k):
    acc_AA = {}
    totalCount = 0
    total = len(testSet)
    label_test = list(set(testLabel))  # 确定有几类
    for label in label_test:
        trueCount = 0
        X1 = np.array([testSet[i] for i in range(len(testSet)) if testLabel[i] == label])
        for j in range(len(X1)):
            label_ = knn(trainSet,trainLabel,X1[j],k)
            if label_ == label:
                trueCount += 1
        totalCount += trueCount
        acc_AA[label] = float(trueCount)/float(len(X1))
    acc_OA = float(totalCount) / float(total)
    return acc_AA,acc_OA

# 确定最优k值
def best_k(train_set,test_set,dimension):
    k_range = range(1, 31, 2)
    k_acc = []
    for k in k_range:
        acc = 0
        for i in range(0, 10):
            X_train, Y_train, X_test, Y_test = LDA_return(train_set[i], test_set[i], dimension)
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








