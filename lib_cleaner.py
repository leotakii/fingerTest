## Versao modificada de Bruno Serbena
from PIL import Image
import numpy as np
from scipy import ndimage, misc, signal
import scipy
import matplotlib.pyplot as plt
import matplotlib.cm
import cv2
import math
import sys

def binarize(img, blk_sz=3):
	img = img.copy()
	#percentileBlack = np.percentile(img, 78)
	#percentileWhite = np.percentile(img, 90)
	percentileBlack = np.percentile(img, 78)
	percentileWhite = np.percentile(img, 89)
	print('percentileBlack',percentileBlack)

	print('percentileWhite',percentileWhite)

	#print(percentileWhite)

	#hist, bins = np.histogram(img, 256, [0, 256])
	#plt.hist(img.ravel(), 256, [0, 256])
	#plt.title('Histogram for gray scale picture')
	#plt.show()
	means = np.zeros(img.shape)

	# number of blocks in a dimension
	blk_no_y, blk_no_x = (int(img.shape[0]//blk_sz), int(img.shape[1]//blk_sz))
	blk_mean = np.zeros((blk_no_y, blk_no_x))
	# for each block i,j
	for i in range(blk_no_y):
		for j in range(blk_no_x):
			block = img[blk_sz*i: blk_sz*(i+1), blk_sz*j: blk_sz*(j+1)]
			blk_mean[i, j] = np.mean(block)
		 
	img = np.where(img < percentileBlack, 0, img)
	img = np.where(img >= percentileWhite, 255, img)

	#plt.imshow(img,cmap="gray")
	#plt.show()
	for i in range(1, img.shape[0]-1):
		for j in range(1, img.shape[1]-1):
			if(img[i, j] == 0 or img[i, j] == 255):
				continue
			block = img[i-1: i+1+1, j-1: j+1+1]
			block = np.ma.array(block.flatten(), mask=False)
			block.mask[len(block)//2] = True
			#print(block.mean())
			 
			if(block.mean() >= blk_mean[i//blk_sz, j//blk_sz]):
				img[i, j] = 0
			else:
				# img[i, j] = 255
				# better
				img[i, j] = 255
	#plt.imshow(img,cmap="gray")
	#plt.show()
	return img


def smooth_bin_filter(img, blk_sz, fil_sz, thresh):
   img_smo = img.copy()
   for i in range(fil_sz, img.shape[0]-fil_sz):
      for j in range(fil_sz, img.shape[1]-fil_sz):
         block = img[i - fil_sz: i+fil_sz+1, j-fil_sz: j+fil_sz+1]
         #print(block.shape)
         black_no = np.sum(block)
         white_no = fil_sz**2 - black_no
         if(black_no >= thresh):
            img_smo[i, j] = 1
         if(white_no >= thresh):
            img_smo[i, j] = 0
   return img_smo

def smooth_bin(img, blk_sz):
   img_smo = img.copy()
   #for fil_sz, thresh in [(3, 18),(1, 5)]:
   img_smo = smooth_bin_filter(img, blk_sz, 2, 20) ##efetuando filtro 5x5
   img_smo = smooth_bin_filter(img, blk_sz, 1, 2) ##efetuando filtro 3x3
   #for fil_sz, thresh in [(3, 5),(1, 3)]:
   #   img_smo = smooth_bin_filter(img, blk_sz, fil_sz, thresh)

   return img_smo
