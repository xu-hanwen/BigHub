import cv2
from numpy import *
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize

# 归一化
def Std(arr):
    u = np.mean(arr)
    s = np.std(arr)
    arr = (arr-u)/s
    return arr

# 数据读取
def image_read():
    Data = np.zeros(6401)
    for i in range(1, 16):
        for j in range(1, 12):
            img = cv2.imread(str(i)+'_s'+str(j)+'.bmp', cv2.IMREAD_GRAYSCALE)
            img_flat = img.reshape((1, img.shape[0] * img.shape[1],))
            img_flat = np.squeeze(img_flat)
            img_flat = Std(img_flat)
            img_flat = np.append(img_flat, i)
            Data = np.vstack((Data, img_flat))
    Data = Data[1:, :]
    print(np.shape(Data))
    return Data


def random_split(dateSet):
    """随机拆分数据集"""
    train_set, test_set = train_test_split(dateSet, test_size=0.2, random_state=None)
    return train_set, test_set


def show_accuracy(prediction, label):
    count = 0
    for i in range(len(prediction)):
        if label[i] == prediction[i]:
            count = count+1
    print(count/len(prediction))


# step 1: load data
print("step 1: load data...")

dataSet = image_read()
trainSet, testSet = random_split(dataSet)

train_x = trainSet[:, 0:6400]
train_y = trainSet[:, -1]
test_x = testSet[:, 0:6400]
test_y = testSet[:, -1]

# step 2: training...
print("step 2: training...")
# clf = svm.SVC(C=0.2, kernel='linear', decision_function_shape='ovr')
clf = svm.SVC(C=1.5, kernel='rbf', decision_function_shape='ovr')
# clf = svm.SVC(C=0.9, kernel='poly', degree=2, coef0=10)
clf.fit(train_x, train_y.ravel())

# step 3: testing
print("step 3: testing...")

print("训练集")
# print(clf.score(train_x, train_y))
y_hat = clf.predict(train_x)
show_accuracy(y_hat, train_y)

print("测试集")
# print(clf.score(test_x, test_y))
y_hat = clf.predict(test_x)
show_accuracy(y_hat, test_y)

# step 4: show the result
# print("step 4: show the result...")
# print('decision_function:\n', clf.decision_function(train_x))
# print('\npredict:\   n', clf.predict(train_x))
