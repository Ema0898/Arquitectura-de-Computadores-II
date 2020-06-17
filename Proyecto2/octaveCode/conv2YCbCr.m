function ycbcr = conv2YCbCr(rgb)
 
  red = rgb(:, :, 1);
  grn = rgb(:, :, 2);
  blu = rgb(:, :, 3);
   
  y   = round((65.738 * red  + 129.057 * grn  + 25.064 * blu) / 256)  + 16;
  cb  = round((-37.945 * red - 74.494 * grn   + 112.439 * blu) / 256) + 128;
  cr  = round((112.439 * red - 94.154 * grn  - 18.285 * blu) / 256)  + 128;
    
  ycbcr(:, :, 1) = y;
  ycbcr(:, :, 2) = cb;
  ycbcr(:, :, 3) = cr;
     
endfunction