%传统PID校正
clc;
clear;
ts=0.001;                 %采样时间  
sys=tf(523500,[1 87.35 10470 0]); %tf是传递函数  即被控对象函数G（）;  
dsys=c2d(sys,ts,'z');    %把控制函数离散化取Z变换n阶定常离散系统差分方程
[num,den]=tfdata(dsys,'v');% 离散化后提取分子、分母    

u_1=0.0; u_2=0.0; u_3=0.0;   %z变换之后的系数
y_1=0.0; y_2=0.0; y_3=0.0;  
x=[0,0,0]';  %分别误差e，误差e的差分，误差e的积分
error_1=0;   %上一时刻误差

time=zeros(1,1000); %预分配内存
yd=zeros(1,1000);
u=zeros(1,1000);
y=zeros(1,1000);
error=zeros(1,1000);

for k=1:1:1000  
time(k)=k*ts;%离散化的时间代表连续时间
yd(k)=1.0;%目标量
kp=0.5;ki=0.001;kd=0.001; % 第一组参数
%kp=0.05; ki=0.01;kd=0.01;  % 第二组参数
%kp=0.2; ki=0.005;kd=0.015;  % 第三组参数
%kp=0.035; ki=0.004;kd=0.03;  % 第四组参数
%kp=0.8; ki=0.014;kd=0.0001;  % 第五组参数
%kp=0.16; ki=0.008;kd=0.0045;  % 第六组参数
%kp=0.0072; ki=0.1;kd=0.1;  % 第七组参数
%kp=0.568; ki=0.081;kd=0.001;  % 第八组参数
%kp=0.56; ki=0.001;kd=0.11;  % 第九组参数
%kp=0.84; ki=0.2;kd=0.0041;  % 第十组参数

u(k)=kp*x(1)+kd*x(2)+ki*x(3);%PID输出

if u(k)>=10
    u(k)=10;
end
 if u(k)<=-10
    u(k)=-10;
 end

%把传递函数转化为差分方程，以实现PID控制。 
y(k)=-den(2)*y_1-den(3)*y_2-den(4)*y_3+num(2)*u_1+num(3)*u_2+num(4)*u_3;          
error(k)=yd(k)-y(k);        % 误差=输入-输出 
u_3=u_2;
u_2=u_1;  %保存上上次输入   为下次计算  
u_1=u(k); %保存上一次控制系数   为下次计算 
y_3=y_2;                                         
y_2=y_1;        %保存上上次次输出   为下次计算  
y_1=y(k);    %保存上一次输出   为下次计算  

x(1)=error(k);                  %KP的系数  
x(2)=(error(k)-error_1)/ts;     %KD的系数  
x(3)=x(3)+error(k)*ts;          %KI的系数
error_1=error(k);                 
end 

figure(1);  
plot(time,yd,'b',time,y,'r');               %输入和实际控制输出  
xlabel('time(s)'),ylabel('y,yd');   
title('输入/输出图像对比')
figure(2);  
plot(time,error,'r')                            %时间误差输出曲线  
xlabel('time(s)');ylabel('error'); 
title('误差变化')