import cv2
import numpy
#from matplotlib import pyplot

im_orig = cv2.imread('Pictures/crowd.png')
#im_gray = cv2.cvtColor(im_orig, cv2.COLOR_BGR2GRAY)
template = cv2.imread('Pictures/ryan_profile',0)
w, h = template.shape[::-1]

res = cv2.matchTemplate(img_orig, template,vc2.TM_CCOEFF_NORMED)
threashold = 0.8
loc = np.where( res >= threadhold)
print(loc)
#for pyplot in zip(*loc[::-1]):
#	cv2.rectangle(img_orig, pt, (pt[0] + w, pt[1] + h),(0,0,255),2)
	
#cv2.imwrite('Pcitures/res.png',img_orig)