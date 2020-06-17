function rgb = conv2RGB(ycbcr)
 
  y = ycbcr(:,:,1);
  cb = ycbcr(:,:,2);
  cr = ycbcr(:,:,3);
   
  r  = round(y  +  1.4 * (cr - 128));
  g  = round(y - 0.343 * (cb - 128) - 0.711 * (cr - 128));
  b  = round(y + 1.765 * (cb - 128));
    
  rgb(:,:,1) = r;
  rgb(:,:,2) = g;
  rgb(:,:,3) = b;
     
endfunction