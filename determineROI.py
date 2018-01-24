#########################
#View image in matplotlib to determine pixels

img = cv2.imread('frame0.jpg', 1) #Reference frame with blackout already saved. Use code in videoAnalysis.py to do this
plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show() 
cv2.imshow('frame0', img)
cv2.waitKey(0) #waits for any key press
cv2.destroyAllWindows