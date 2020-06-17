function ycbcr = bitwise(rgb)
 
  red = rgb(:, :, 1);
  grn = rgb(:, :, 2);
  blu = rgb(:, :, 3);

  y_r = bitshift(red, 6) + bitshift(red, 1);
  y_g =  bitshift(grn, 7) + grn;
  y_b = bitshift(blu, 3) + blu;

  cb_r = -1 * (bitshift(red, 5) + bitshift(red, 2) + bitshift(red, 1));
  cb_g = -1 * (bitshift(grn, 6) + bitshift(grn, 3) + bitshift(grn, 1));
  cb_b = bitshift(blu, 7) - bitshift(blu, 4);

  cr_r = bitshift(red, 7) - bitshift(red, 4);
  cr_g = -1 * (bitshift(grn, 6) + bitshift(grn, 5) - bitshift(grn, 1));
  cr_b = -1 * (bitshift(blu, 4) + bitshift(blu, 1));
   
  y   = 16 + bitshift((y_r + y_g + y_b), -8); 
  cb  = 128 + bitshift((cb_r + cb_b + cb_g), -8);
  cr  = 128 + bitshift((cr_r + cr_g + cr_b), -8);
    
  ycbcr(:, :, 1) = y;
  ycbcr(:, :, 2) = cb;
  ycbcr(:, :, 3) = cr;
     
endfunction