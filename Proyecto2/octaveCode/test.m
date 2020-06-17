clc; clear;
pkg load image;

A = imread('img/mono.png');

A = double(A);

tic
B = conv2YCbCr(A);
t1 = toc

tic
C = bitwise(A);
t2 = toc

A = uint8(A);
B = uint8(B);
C = uint8(C);

subplot(1, 3, 1);
imshow(A);
title('Original Image');

subplot(1, 3, 2);
imshow(B);
title('YCBCR Image');

subplot(1, 3, 3);
imshow(C);
title('YCBCR Image (bitwise)');