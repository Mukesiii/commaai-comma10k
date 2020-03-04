#!/usr/bin/env python3
import os
import sys
sys.path.append(os.getcwd())
import numpy as np
from viewer import fix, get_colormap
from tqdm import tqdm
from multiprocessing import Pool
from PIL import Image

colormap = get_colormap()

def canon_mask(x):
  segi = fix(Image.open("masks/"+x))

  #print(x, segi.shape, segi.dtype)
  check = segi.reshape(-1, 3)

  ok = np.zeros(check.shape[0], dtype=np.bool)
  for v in colormap.values():
    okk = check == np.array(v)
    okk = np.all(okk, axis=1)
    ok |= okk

  if not np.all(ok):
    print(x+" HAS %d pixels with BAD COLORS" % sum(np.logical_not(ok)))
    print(check[np.logical_not(ok)])
    """
    cva = np.array(list(colormap.values()))
    maxb = 0
    for i in np.argwhere(np.logical_not(ok)):
      vv = np.mean((check[i] - cva)**2, axis=1)
      col = np.argmin(vv)
      maxb = max(vv[col], maxb)
      if maxb >= 20:
        break
      #print(i, check[i], col, vv[col])
      check[i] = cva[col]
    if maxb < 20:
      print("FIXED", maxb)
      segi = check.reshape(segi.shape)
    else:
      print("COULDN'T FIX", maxb)
    """

  im = Image.fromarray(segi)
  im.save("masks/"+x)

  #os.rename("masks/_"+x, "masks/"+x)

if __name__ == "__main__":
  lst = sorted(os.listdir("masks/"))
  if len(sys.argv) > 1:
    canon_mask(lst[int(sys.argv[1])])
    exit(0)

  p = Pool(16)
  for _ in tqdm(p.imap_unordered(canon_mask, lst), total=len(lst)):
    pass

