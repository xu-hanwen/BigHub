% 画出系统的单位阶跃响应
clc;
clear;

sys=tf(523500,[1 87.35 10470 0]);
sysc=feedback(sys,1);
step(sysc)