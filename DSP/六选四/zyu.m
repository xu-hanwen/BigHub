x=[1,1,1,1];nx=[0:3];%x(n)=R(n) 
w=linspace(-2.8*pi,2.8*pi,100000);%取100000个点
X=x*exp(-j*nx'*w);%DTFT 
figure(1);
subplot(3,2,1),plot(w/pi,abs(X));xlabel('\omega/\pi');ylabel('|X(e^j^\omega)|')
subplot(3,2,2),plot(w/pi,angle(X));xlabel('\omega/\pi');ylabel('\phi(\omega)/\pi')

%差分方程求解 
a=[1,-0.4];b=[1];
[H,w]=freqz(b,a,'whole');
subplot(3,2,3),plot(w/pi,abs(H));xlabel('\omega/\pi');ylabel('|X(e^j^\omega)|')
subplot(3,2,4),plot(w/pi,angle(H));xlabel('\omega/\pi');ylabel('\phi(\omega)/\pi')

%零极点分布 
a=[1,-1.6,0.9425];%分母 
b1=[1,-0.3];b2=[1,-0.8];%分子
[F,w]=freqz(b1,a,'whole');
figure(2);
subplot(2,2,1),zplane(b1,a);%零极点分布图 
subplot(2,2,3),plot(w/pi,abs(F));xlabel('\omega/\pi');ylabel('|X(e^j^\omega)|')
subplot(2,2,4),plot(w/pi,angle(F));xlabel('\omega/\pi');ylabel('\phi(\omega)/\pi')

figure(3);%改变零极点分布，观察频率响应变化 
[F,w]=freqz(b2,a,'whole');
subplot(2,2,1),zplane(b2,a);
subplot(2,2,3),plot(w/pi,abs(F));xlabel('\omega/\pi');ylabel('|X(e^j^\omega)|')
subplot(2,2,4),plot(w/pi,angle(F));xlabel('\omega/\pi');ylabel('\phi(\omega)/\pi')