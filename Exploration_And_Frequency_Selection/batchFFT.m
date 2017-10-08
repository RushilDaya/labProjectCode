function output = batchFFT(dataVec, sampleRate, batchSize, windowFunc)
%computes a batch fft on a data stream.
%removes the dc component on a batch
% note that batch size is in samples not time
numBatches = floor(length(dataVec)/batchSize);

output.fft = zeros(batchSize/2+1,numBatches);
windowVec = window(windowFunc,batchSize);
for iter = 1:numBatches
    data = dataVec((iter-1)*batchSize+1:(iter-1)*batchSize+batchSize);
    data = data - mean(data);
    data = data.*windowVec;
    DATA = fft(data);
    DATA = DATA(1:batchSize/2+1);
    output.fft(:,iter)=DATA';
end

output.frequency = 0:sampleRate/batchSize:sampleRate/2;
end

