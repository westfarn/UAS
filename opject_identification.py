import cv2
import numpy
import os
from matplotlib import pyplot
import sys


#cmd to call python opject_identification
#return:
#   1 = found something
#   0 means we didn't

def print_image_properties(im,name):
    
	print name
	print(im.shape)
	#print("im.shape[1]: %f" % im.shape[1])
	#print("im.shape[2]: %f" % im.shape[2])
	#print("im.depth: %f" % im.depth)

def circles2(filename='Pictures/test2.jpg'):
	img = cv2.imread(filename,0)
	img = cv2.medianBlur(img,5)
	cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
	#print(type(img))
	circles = cv2.HoughCircles(img, cv2.cv.CV_HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
	
	circles = numpy.uint16(numpy.around(circles))
	
	#for i in circles[0,:]:
		#cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),3)
		#cv2.circle(cimg,(i[0],i[1]),i[2],(0,0,255),3)
	#cv2.imshow('detected circles',cimg)
##	
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()
	
	
	if circles is not None:
		#print circles
		return True
	else:
		return False
#opencv logo
	
def circles(filename='Pictures/test2.jpg'):
	image = cv2.imread(filename)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
	if image is not None:
		for i in range(100,1000):
			for j in range(100,1000):
				circles = cv2.HoughCircles(gray,cv2.cv.CV_HOUGH_GRADIENT,1,1)
				if circles is not None:
					print("Found circles: i = %i | j = %i" % (i,j))
				#	for circle in circles:
				#		print circle
				else:
					pass
					#print("Didn't find any circles")
			print("%f percent complete: " % (int(i)/1000.0 * 100))
	else:
	
		print("the image is none")
		return

def facial_recogni():
		
	orig_filename = 'Pictures/ryan_sam_and_jake.jpg'
	template_filename = 'Pictures/ryan_profile.jpg'
	im_orig = cv2.imread(orig_filename)
	#im_gray = cv2.cvtColor(im_orig, cv2.COLOR_BGR2GRAY)
	template = cv2.imread(template_filename)

	print_image_properties(im_orig,orig_filename)
	print_image_properties(template,template_filename)

	if im_orig == None or type == None:
		
		print("im_orig: ", type(im_orig))
		if not os.path.isfile(orig_filename):
			print "might want to check %s" % orig_filename
		print("template: ", type(template))
		if not os.path.isfile(template_filename):
			print "might want to check %s" % template_filename
	w = template.shape[0]
	h = template.shape[1]

	methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
				'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

	for meth in methods:
		
		method = eval(meth)
		res = cv2.matchTemplate(im_orig, template,method)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		threshold = 0.8
		top_left = 0
		if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
			top_left = min_loc
		else:
			top_left = max_loc
		bottom_right = (top_left[0] + w, top_left[1] + h)
		
		cv2.rectangle(im_orig,top_left,bottom_right,255,2)
		pyplot.subplot(121),pyplot.imshow(res,cmap = 'gray')
		pyplot.title('Matching Result'),pyplot.xticks([]), pyplot.yticks([])
		pyplot.subplot(122),pyplot.imshow(im_orig,cmap = 'gray')
		pyplot.title('Detecte point'),pyplot.xticks([]),pyplot.yticks([])
		pyplot.suptitle(meth)
		
		pyplot.show()
			
		print('min_val: %s' % str(min_val))
		print('max_val: %s' % str(max_val))
		print('min_loc: %s' % str(min_loc))
		print('max_loc: %s' % str(max_loc))
		loc = numpy.where(res >= threshold)
		print '\n'
	
if __name__ == "__main__":
	#test()
	result = 0
	if len(sys.argv) > 1:
		result = circles2(sys.argv[1])
	else:
		result = circles2()
	if result:
		sys.exit(1)
	else:
		sys.exit(0)