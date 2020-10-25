%专家PID控制
clc;
clear;

ts=0.001; % 采样时间
sys=tf(5.235e005,[1,87.35,1.047e004,0]);  % 传递函数
dsys=c2d(sys,ts,'z'); % 连续模型离散化
[num,den]=tfdata(dsys,'v');% 获得分子分母

u_1=0;u_2=0;u_3=0;
y_1=0;y_2=0;y_3=0;

x=[0,0,0]';
x2_1=0;
% 比例积分微分参数
kp=0.6;
ki=0.03;     
kd=0.01;

error_1=0;
for k=1:1:500
time(k)=k*ts;   
r(k)=1.0;                   
% 第k次控制器输出
u(k)=kp*x(1)+kd*x(2)+ki*x(3); 

% 控制误差输出的绝对值，避免超调
if abs(x(1))>0.8                 % 规则1
   u(k)=0.45;
elseif abs(x(1))>0.40        
   u(k)=0.40;
elseif abs(x(1))>0.20    
   u(k)=0.12; 
elseif abs(x(1))>0.01 
   u(k)=0.10;   
end   
% 规则2：误差为某一常数，未发生变化
if x(1)*x(2)>0|(x(2)==0)    
   if abs(x(1))>=0.05
      u(k)=u_1+2*kp*x(1);
   else
      u(k)=u_1+0.4*kp*x(1);
   end
end
% 规则3：误差的绝对值朝减小的方向变化                                                                                                                                                                                                                                                                                                                                                                                                           
if (x(1)*x(2)<0&x(2)*x2_1>0)|(x(1)==0)
    u(k)=u(k);
end
%规则4，误差处于极值状态
if x(1)*x(2)<0&x(2)*x2_1<0 
   if abs(x(1))>=0.05
      u(k)=u_1+2*kp*error_1;
   else
      u(k)=u_1+0.6*kp*error_1;
   end
end
% 规则5，误差的绝对值很小
if abs(x(1))<=0.001   % PI控制
   u(k)=0.5*x(1)+0.010*x(3);
end

% 控制输出
if u(k)>=10
   u(k)=10;
end
if u(k)<=-10
   u(k)=-10;
end

%线性模型  Z变换
y(k)=-den(2)*y_1-den(3)*y_2-den(4)*y_3+num(1)*u(k)+num(2)*u_1+num(3)*u_2+num(4)*u_3;
error(k)=r(k)-y(k);

%Return PID parameters
u_3=u_2;u_2=u_1;u_1=u(k);
y_3=y_2;y_2=y_1;y_1=y(k);
   
x(1)=error(k);                % P
x2_1=x(2);
x(2)=(error(k)-error_1)/ts;   % D
x(3)=x(3)+error(k)*ts;        % I

error_1=error(k);
end
figure(1);
plot(time,r,'b',time,y,'r');
xlabel('time(s)');ylabel('r,y');
grid on
title('PID控制阶跃响应曲线')
figure(2);
plot(time,r-y,'r');
xlabel('time(s)');ylabel('error');
grid on
title('误差响应曲线')
