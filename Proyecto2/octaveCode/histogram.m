clc; clear;

Z  = imread('img/mono.png');

Z = double(Z);

X = bitwise(Z);

A = X(:, :, 1);

Z = uint8(Z);

subplot(2, 2, 1);
imshow(Z);

[m, n] = size(A);

% Calcular el histograma
h2 = zeros(256, 1);
for i = 0 : 255
  h2(i + 1) = sum(sum(A == i));
endfor

subplot(2, 2, 2);
bar(0:255, h2);
title('Histograma');
xlim([0 255]);

% Distribucion acumulada
ac = zeros(256, 1);
for i = 0 : 255
  ac(i + 1) = sum(h2(1 : i + 1)) / (m * n);
endfor

% Obtener la nueva imagen aplicando la tecnica de ecualizacion
B = zeros(m, n);

for i = 1 : m
  for j = 1 : n
    B(i, j) = round(ac(A(i, j) + 1) * 255); 
  endfor
endfor


% Calcular el histograma
h3 = zeros(256, 1);
for i = 0 : 255
  h3(i + 1) = sum(sum(B == i));
endfor

B(:, :, 2) = X(:, :, 2);
B(:, :, 3) = X(:, :, 3);

C = conv2RGB(B);

C = uint8(C);

subplot(2, 2, 3);
imshow(C);

subplot(2, 2, 4);
bar(0:255, h3);
title('Histograma');
xlim([0 255]);
