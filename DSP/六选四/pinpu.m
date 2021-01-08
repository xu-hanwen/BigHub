%IFFT FFT 
x=[0,1,2,3,4,5];
N=8;
X=fft(x,N);
x=ifft(X,N);
figure(1)
subplot(2,1,1)
n=0:1:7;
stem(n,abs(x)),xlabel('n'),ylabel('|x(n)|');
subplot(2,1,2),stem(n,angle(x)),xlabel('n'),ylabel('\phi[x(n)]');

figure(2)
subplot(2,1,1)
n=0:1:7;
stem(n,abs(X)),xlabel('k'),ylabel('|X(k)|');
subplot(2,1,2),stem(n,angle(X)/pi),xlabel('k'),ylabel('\phi[X(k)]/\pi');

%利用FFT和IFFT算法计算系统的输出响应 
h=[1,1,1,1];
x=[1,1,1,1,1];
for j=-1:1:2
    L=8-j;
    y=ifft(fft(h,L).*fft(x,L));
    i=0:1:L-1
    figure(3)
    subplot(4,1,j+2)
    stem(i,y);
end

%采样 
n=0:1:7
f=sin(n*0.25*pi)+cos(n*0.25*pi)
F=fft(f,8);
figure(4)
subplot(2,1,1)
stem(n,abs(F))
subplot(2,1,2)
stem(n,angle(F))