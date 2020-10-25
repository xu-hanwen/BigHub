import os
import torch
import torchvision
import numpy as np
from time import time
import matplotlib.pyplot as plt
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.tensorboard import SummaryWriter

def data_loader():
    """加载数据并数据增强"""
    train_trans = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.RandomGrayscale(),
        transforms.ToTensor()
    ])
    test_trans = transforms.ToTensor()
    url = './Data'
    trainset = torchvision.datasets.FashionMNIST(root=url,train=True,download=True,transform=train_trans)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=100,
                                              shuffle=True, num_workers=4)
    testset = torchvision.datasets.FashionMNIST(root=url,train=False,download=True,transform=test_trans)
    testloader = torch.utils.data.DataLoader(testset, batch_size=100,
                                             shuffle=False, num_workers=4)
    # print(len(trainset),len(testset))
    # feature,label = trainset[0]
    # print(feature.shape,label)
    return trainloader,testloader

def imshow(trainloader):
    """可视化数据"""
    classes_names = ['t-shirt', 'trouser', 'pullover', 'dress', 'coat',
                   'sandal', 'shirt', 'sneaker', 'bag', 'ankle boot']

    plt.figure(figsize=(10,10))
    dataiter = iter(trainloader)
    features,labels = dataiter.next()
    print(features.shape)
    for i in range(10):
        plt.subplot(1,10,i+1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        npimg = features[i].numpy()
        plt.imshow(np.transpose(npimg, (1, 2, 0)))
        plt.xlabel(classes_names[labels[i]])
    plt.show()

class Net(nn.Module):
    """网络模型"""
    def __init__(self):
        super().__init__()
        self.conv1 =  nn.Conv2d(1,6,5)
        self.pool = nn.MaxPool2d(2,2)
        self.bn1 = nn.BatchNorm2d(6)
        self.conv2 = nn.Conv2d(6,16,5)
        self.bn2 = nn.BatchNorm2d(16)
        self.fc1 = nn.Linear(16*4*4,120)
        self.bn3 = nn.BatchNorm1d(120)
        self.fc3 = nn.Linear(120,10)
        # self.fc2 = nn.Linear(120,84)
        # self.bn4 = nn.BatchNorm1d(84)
        # self.fc3 = nn.Linear(84,10)

    def forward(self,x):
        x= self.pool(self.conv1(x))
        x = F.relu(self.bn1(x))
        # x = self.bn1(self.conv1(x))
        # x = self.pool(F.relu(x))
        x = self.pool(self.conv2(x))
        x = F.relu(self.bn2(x))
        # x = self.bn2(self.conv2(x))
        # x = self.pool(F.relu(x))
        x = x.view(-1, 16 * 4 * 4)
        x = F.relu(self.bn3(self.fc1(x)))
        x = F.dropout(x)
        # x = F.relu(self.bn4(self.fc2(x)))
        # x = F.dropout(F.relu(self.fc2(x)))
        x = self.fc3(x)
        return x

    def evaluate_acc(self,criterion,test_iter, device):
        """模型测试"""
        acc_sum, n, test_loss,batch_cont = 0.0, 0,0.0,0
        with torch.no_grad():
            for X, y in test_iter:
                self.eval()
                acc_sum += (self(X.to(device)).argmax(dim=1) == y.to(device)).float().sum().item()
                loss = criterion(self(X.to(device)), y.to(device))
                test_loss += loss.item()
                self.train()
                n += y.shape[0]
                batch_cont += 1
            test_loss = test_loss/batch_cont
            acc_sum = acc_sum/n
        return test_loss,acc_sum

    def train_model(self,device,num_epochs,PATH,lr):
        """模型训练"""
        train_iter,test_iter = data_loader()
        writer = SummaryWriter()
        # writer.add_graph(net, torch.Tensor([1,28,28]))
        # print(net)
        start_epoch = 0
        optimizer = torch.optim.Adam(net.parameters(), lr=lr,weight_decay=0)
        if os.path.exists(PATH) is not True:
            criterion = nn.CrossEntropyLoss()
        else:
            checkpoint = torch.load(PATH)
            self.load_state_dict(checkpoint['model_state_dict'])
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            start_epoch = checkpoint['epoch']
            criterion = checkpoint['criterion']
        # print(lr,start_epoch)

        for epoch in range(start_epoch,num_epochs):
            train_loss, train_acc, n, batch_count,start = 0.0, 0.0, 0, 0,time()

            for features, labels in train_iter:
                features,labels = features.to(device), labels.to(device)
                outputs = self(features)
                # outputs = self.forward(features)
                loss = criterion(outputs, labels)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                train_loss += loss.item()
                train_acc += (outputs.argmax(dim=1) == labels).sum().item()
                n += labels.shape[0]
                batch_count += 1

            test_loss, test_acc = self.evaluate_acc(criterion,test_iter,device)
            print('epoch %d, loss: %.4f, train acc: %d%%, test acc: %d%%, time %.1f sec'
                      % (epoch + 1, train_loss / batch_count, 100 * train_acc / n, 100* test_acc, time()-start))
            writer.add_scalar('train_acc', train_acc, epoch)
            writer.add_scalar('test_acc',test_acc,epoch)
            writer.add_scalar('test_loss', test_loss, epoch)
            writer.add_scalar('train_loss', train_loss/batch_count, epoch)

            if epoch % 10 == 0:
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': net.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'criterion':criterion
                }, PATH)
        writer.close()
        print('Finished Training')

class Net_2(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 5, 1, 2)
        self.norm1 = nn.BatchNorm2d(32)
        nn.init.xavier_uniform(self.conv1.weight)
        self.maxpool1 = nn.MaxPool2d(kernel_size=2)

        self.conv2 = nn.Conv2d(32, 64, 3, 1, 2)
        self.norm2 = nn.BatchNorm2d(64)
        nn.init.xavier_uniform(self.conv2.weight)
        self.maxpool2 = nn.MaxPool2d(2, 2)


        self.fc1 = nn.Linear(4096,4096)
        self.fc2 = nn.Linear(4096, 10)

    def forward(self, x):
        out = F.relu(self.conv1(x))
        out = self.norm1(out)
        out = self.maxpool1(out)

        out = F.relu(self.conv2(out))
        out = self.norm2(out)
        out = self.maxpool2(out)

        out = out.view(out.size(0),-1)
        out = F.relu(self.fc1(out))
        out = self.fc2(out)
        return out

    def evaluate_acc(self,criterion,test_iter, device):
        """模型测试"""
        acc_sum, n, test_loss,batch_cont = 0.0, 0,0.0,0
        with torch.no_grad():
            for X, y in test_iter:
                self.eval()
                acc_sum += (self(X.to(device)).argmax(dim=1) == y.to(device)).float().sum().item()
                loss = criterion(self(X.to(device)), y.to(device))
                test_loss += loss.item()
                self.train()
                n += y.shape[0]
                batch_cont += 1
            test_loss = test_loss/batch_cont
            acc_sum = acc_sum/n
        return test_loss,acc_sum

    def train_model(self,device,num_epochs,PATH):
        """模型训练"""
        train_iter,test_iter = data_loader()
        writer = SummaryWriter()
        # writer.add_graph(net, torch.Tensor([1,28,28]))
        # print(net)
        start_epoch = 0
        optimizer = torch.optim.SGD(net.parameters(), lr=0.015, momentum=0.9, nesterov=True)
        if os.path.exists(PATH) is not True:
            criterion = nn.CrossEntropyLoss()
        else:
            checkpoint = torch.load(PATH)
            self.load_state_dict(checkpoint['model_state_dict'])
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            start_epoch = checkpoint['epoch']
            criterion = checkpoint['criterion']
        # print(lr,start_epoch)

        for epoch in range(start_epoch,num_epochs):
            train_loss, train_acc, n, batch_count,start = 0.0, 0.0, 0, 0,time()

            for features, labels in train_iter:
                features,labels = features.to(device), labels.to(device)
                outputs = self(features)
                # outputs = self.forward(features)
                loss = criterion(outputs, labels)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                train_loss += loss.item()
                train_acc += (outputs.argmax(dim=1) == labels).sum().item()
                n += labels.shape[0]
                batch_count += 1

            test_loss, test_acc = self.evaluate_acc(criterion,test_iter,device)
            print('epoch %d, loss: %.4f, train acc: .2%f%%, test acc: %.2f%%, time %.1f sec'
                      % (epoch + 1, train_loss / batch_count, 100 * train_acc / n, 100* test_acc, time()-start))
            writer.add_scalar('train_acc', train_acc, epoch)
            writer.add_scalar('test_acc',test_acc,epoch)
            writer.add_scalar('test_loss', test_loss, epoch)
            writer.add_scalar('train_loss', train_loss/batch_count, epoch)

            if epoch % 10 == 0:
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': net.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'criterion':criterion
                }, PATH)
        writer.close()
        print('Finished Training')


if __name__ == '__main__':

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # print(device)
    # net = Net()
    net = Net_2()
    net = net.to(device)
    num_epochs = 50
    learning_rate = 0.001
    model_path = './check_point/check_point.tar'

    net.train_model(device,num_epochs,model_path)


