a=0.8,ys=0;
xn=[1,zeros(1,30)];
B=1,A=[1,-a];
xi=filtic(B,A,ys);
hn=filter(B,A,xn,xi);
n=0:length(hn)-1;
subplot(2,2,1);
stem(n,hn,'.');
title('系统单位脉冲响应');xlabel('n');ylabel('h(n)')

xn=ones(1,30);%单位阶跃序列 
sn=filter(B,A,xn,xi);
n=0:length(sn)-1;
subplot(2,2,2);
stem(n,sn,'.');
title('系统单位阶跃响应');xlabel('n');ylabel('s(n)')

x=[1,zeros(1,30)];
vn=conv(x,hn);
n=0:length(vn)-1;
subplot(2,2,3);
stem(n,vn,'.');
title('零状态单位阶跃响应');xlabel('n');ylabel('v(n)')