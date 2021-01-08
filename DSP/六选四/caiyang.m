clear all;
close all;

T=0.001;tf=0.1;t=-tf:T:tf;%建立连续自变量向量
xa=sin(2*pi*50*t)+cos(2*pi*100*t);%产生模拟信号, 由t的取值知xa有201个值
w=linspace(-2*pi,2*pi,100);%在[-2pi,2pi]区间均匀取100个点
nx=0:200;

figure(1);
subplot(2,2,1),plot(t,xa);%原模拟信号的波形
title('原模拟信号波形');

fs1=120;Ts1=1/fs1;%设置欠采样频率 fs<2fm
fs3=240;Ts3=1/fs3;%设置过采样频率 fs>2fm
n1=-tf/Ts1:tf/Ts1;   %设置采样点
n3=-tf/Ts3:tf/Ts3;
m1=0:2*tf/Ts1;
m3=0:2*tf/Ts3;

x1=sin(2*pi*50*n1*Ts1)+cos(2*pi*100*n1*Ts1); %产生欠采样信号
x3=sin(2*pi*50*n3*Ts3)+cos(2*pi*100*n3*Ts3);   %过采样信号
subplot(2,2,2);
stem(n1,x1, 'r-');%绘制欠采样信号波形
title('欠采样信号波形');
subplot(2,2,3);
stem(n3,x3,'r-'); %绘制过采样信号波形
title('过采样信号波形');