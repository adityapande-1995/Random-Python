#!python3
import cv2
import numpy as np

class Scanner:
    def __init__(self):
        self.raw_image = None
        self.resized_image = None
        self.highlight_paper = None
        self.paper_coords = None
    
    def load_image(self,img_path,scale=1):
        print("Loading image..")
        self.raw_image = cv2.imread(img_path) # Raw image
        self.resized_image = cv2.resize(self.raw_image, (0,0), fx=scale, fy=scale)  # Resized image
    
    def autodetect_paper(self):
        print("Trying to locate the paper..")
        gray = cv2.cvtColor(self.resized_image.copy(), cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 75, 200)

        _, contours, _ = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        for c in contours: # approximate the contour
	        peri = cv2.arcLength(c, True)
	        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            # if the approximated contour has four points, then we can assume that we have found our screen
	        if len(approx) == 4:
		        screenCnt = approx
		        break

        self.highlight_paper = self.resized_image.copy() # Resized image  with autocontours highlighted
        cv2.drawContours(self.highlight_paper , [screenCnt], -1, (0, 255, 0), 2)
        self.paper_coords = np.reshape(screenCnt,(4,2))  # Coordinates of the paper

        # Label vertices
        for i in range(0,len(self.paper_coords)):
            cv2.circle(self.highlight_paper,(self.paper_coords[i,0], self.paper_coords[i,1]), 5, (0,0,255), -1)
            cv2.putText(self.highlight_paper,str(i)+str(self.paper_coords[i]),(self.paper_coords[i,0]+5, self.paper_coords[i,1]+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,255,255),1)

    def manual_paper(self):
        print("Specify paper coordinates manually")
    
    def pers_transform(self,thresh=True):
        p1 = np.float32(self.paper_coords)
        width = int(np.sqrt( (p1[0,0] - p1[1,0])**2 + (p1[0,1] - p1[1,1])**2 ) )
        height = int(np.sqrt( (p1[1,0] - p1[2,0])**2 + (p1[1,1] - p1[2,1])**2 ) )
        p2 = np.float32([[0,0],[width,0],[width,height],[0,height]])
        M = cv2.getPerspectiveTransform(p1,p2)
        # print("Old pts: ",p1," New pts: ",p2)
        dst = cv2.warpPerspective(self.resized_image.copy(),M,(width,height))

        if thresh:
            # Threshold 
            th3 = cv2.adaptiveThreshold(cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
            self.final = th3
        else:
            self.final = dst
    
    def correct_orientation(self):
        done = False
        print("Enter changes to be made: \nh- mirror horizontal, \nv- mirror vertical, \nr-rotate 90deg clockwise, \nd-Exit")
        while not done:
            cv2.imshow("demo", self.final) 
            action = cv2.waitKey(0)
            if action == ord("d"):
                done = True
            elif action == ord("h"):
                self.final = cv2.flip(self.final, 1)
            elif action == ord("v"):
                self.final = cv2.flip(self.final, 0)
            elif action == ord("r"):
                print("WIP")


# Main
A = Scanner()
A.load_image("3.jpg",1)
A.autodetect_paper()

print("Has the paper been detected correctly? Press(y/n)")
cv2.imshow("demo", A.highlight_paper) 
key = cv2.waitKey(0)
if key == ord("n"):
    A.manual_paper() # WIP

A.pers_transform(thresh=False)
A.correct_orientation()
