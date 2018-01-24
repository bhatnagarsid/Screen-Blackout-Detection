#Breaks down videos into frames, saves frames to file, and checks if blackout occurred

import numpy as np
import cv2
import pprint
import time
from matplotlib import pyplot as plt 
from statistics import mode

#Checking Hour 24 to Hour 48
ITERATIONS_24HR = 1300000 #Running at 15fps, 24hrs*60min/hr*60sec/min*15frames/sec = 1,296,000
ITERATIONS_48HR = 2600000 #Running at 15fps, 48hr*60min/hr*60sec/min*15 = 2,592,000
BLACKOUT_THRESHOLD = 75 #56 #See Choosing_Blackout_Threshold.txt 
c1 = 171 #Chosen using determineROI script to plot frame and find appropriate pixel range 
r1 = 82

print(cv2.__version__)
t0 = time.time()
vidcap = cv2.VideoCapture('2017-11-03-Test-Copy.mp4') #Video file on local disk of student laptop
success,image = vidcap.read()
print(success) #Check if vidcap.read() worked 
count = 0 
avg = [] 
frames_avgRoi = []
f = open('Frames_Hr24toHr48.txt', 'w')
f.write('The following pairs are frames with the corresponding average ROI values with potential blackout. \n')  

#To check HR24 to HR48. Last frame check with 24HR test is 1,299,999, thus start at 1,300,002
count = 1561011
frame_no = 1561011  
vidcap.set(1,frame_no) #Use 1 to choose 2nd Parameter of Function CAP_PROP_POS_FRAMES, sets frame to be decoded/captured next  

while count < ITERATIONS_48HR:
	success,image = vidcap.read()
	if success == False:
		print('Frame read failed, exiting loop\n')
		break 
	if count%3 == 0: #Since blackout usually last 1-2 seconds, check every 3rd frame. Reduces computation time 
		cv2.imwrite("frame%d.jpg" % count, image)
		sublist = []
		roi = image[c1:c1+239,r1:r1+96] # sets region of interest in frame that was read from the video file, c1,r1 are column and row locations
		avg.append(roi.mean())
		if(roi.mean() < BLACKOUT_THRESHOLD) :
			f.write('{0} with ROI avg of {1}\n'.format(count, roi.mean()))
			sublist.append((count,(roi.mean()).round()))
			frames_avgRoi.append(sublist)
	if((((count/ITERATIONS_48HR)*100)%5) == 0) : #Updating console every 5% 
		print('Completed', (((count/ITERATIONS_48HR)*100)), '%, frames:', count)
	count += 1	

t1 = time.time() 
total = t1-t0 
print('Execution time:', total)
print(frames_avgRoi) 
f.close() 

