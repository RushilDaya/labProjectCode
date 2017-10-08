%% Show the frequencies acheivable on the sender side
% actual up and down times are shown in the accompaning 
% spread sheet. Change samples to affect window size.
% from the plot the desired number of frequencies can 
% be chosen. aim to minimize the overlap between frequencies



SAMPLES = 512;
TIME = SAMPLES/128;

A = sin(25*linspace(0,TIME*2*pi,SAMPLES));
A = [A, sin(31.25*linspace(0,TIME*2*pi,SAMPLES)) ];
A = [A, sin(23.25558*linspace(0,TIME*2*pi,SAMPLES)) ];
A = [A, sin(32.5806*linspace(0,TIME*2*pi,SAMPLES)) ];
A = [A, sin(34.482*linspace(0,TIME*2*pi,SAMPLES)) ];
A = [A, sin(27.027*linspace(0,TIME*2*pi,SAMPLES)) ];
A = [A, sin(27.7777*linspace(0,TIME*2*pi,SAMPLES)) ];
A = [A, sin(35.714*linspace(0,TIME*2*pi,SAMPLES)) ];
A = [A, sin(37.037*linspace(0,TIME*2*pi,SAMPLES)) ];
A = [A, sin(38.46*linspace(0,TIME*2*pi,SAMPLES)) ];
A = [A, sin(30.30*linspace(0,TIME*2*pi,SAMPLES)) ];
A = [A, sin(23.81*linspace(0,TIME*2*pi,SAMPLES)) ];
A = [A, sin(26.32*linspace(0,TIME*2*pi,SAMPLES)) ];
A = [A, sin(28.57*linspace(0,TIME*2*pi,SAMPLES)) ];
A = [A, sin(33.33*linspace(0,TIME*2*pi,SAMPLES)) ];
A = [A, sin(29.41*linspace(0,TIME*2*pi,SAMPLES)) ];
A = [A, sin(25.64*linspace(0,TIME*2*pi,SAMPLES)) ];
A = [A, sin(24.39*linspace(0,TIME*2*pi,SAMPLES)) ];
Q = batchFFT(A',128,SAMPLES,'hann');


figure, plot(Q.frequency,abs(Q.fft));