import cv2
import numpy as np
from FCM import FCM
import data_process as dp
from K_Means import K_means
import matplotlib.pyplot as plt

def data_cluster():
    """对Iris、Sonar聚类"""
    url = 'Data/iris/iris.data'   # iris_oa_max_k-means=0.89 ,iris_oa_max_FCM = 0.89
    # url = 'Data/sonar/sonar.all-data'  # sonar_oa_max_k-means = 0.56,sonar_oa_max_FCM = 0.55
    dateset = dp.load_dataset(url)
    feature, label = dp.frame_select(dateset)
    k = 3

    # FCM
    alpha = 2
    Fcm = FCM(k,feature,alpha)
    acc_oa,acc_aa = Fcm.evaluate(label)
    center_array = np.array(Fcm.class_centers)
    print('acc_oa_fcm:{},acc_aa_fcm:{}'.format(acc_oa, acc_aa))
    Fcm.plot(feature, label)

    # k-means
    k_means = K_means(feature, k)
    acc_oa, acc_aa = k_means.evaluate(feature, label)
    print('acc_oa_k-means:{},acc_aa_fcm:{}'.format(acc_oa, acc_aa))
    k_means.plot(k_means.centers, feature, label)

def draw(img,img_flat,lables_):
    # 重新上色
    for o in range(len(img_flat)):
        # 根据类别信息拆分数据
        if lables_[o] == 0:
            img_flat[o] = [0,0,255]
        elif lables_[o] == 1:
            img_flat[o] = [0,255,0]
        elif lables_[o] == 2:
            img_flat[o] = [255,0,0]

    img_output = np.array(img_flat).reshape((img.shape[0],img.shape[1],3))
    img_output = img_output/255  # 归一化
    return img_output

def picture_cluster():
    """对图片进行聚类"""
    img = cv2.imread('pictures/3.bmp')
    b,g,r = cv2.split(img)
    img = cv2.merge([r,g,b])
    # 像素展平
    img_flat = img.reshape((img.shape[0]*img.shape[1],3))
    img_flat_1 = np.float32(img_flat)
    img_flat_2 = np.float32(img_flat)

    #k-means
    k = 3
    k_means = K_means(img_flat_1, k)
    lables_ = k_means.predict(img_flat_1)
    img_output = draw(img, img_flat_1,lables_)
    plt.subplot(311), plt.imshow(img), plt.title('input')
    plt.subplot(312), plt.imshow(img_output), plt.title('k-means')

    # FCM
    alpha = 2
    Fcm = FCM(k, img_flat_2, alpha)
    lables_ = Fcm.predict()
    img_output = draw(img,img_flat_2,lables_)
    plt.subplot(313),plt.imshow(img_output),plt.title('fcm')
    plt.show()

if __name__ == '__main__':
    data_cluster()
    picture_cluster()

