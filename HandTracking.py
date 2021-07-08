import cv2
import mediapipe as mp
import time
from math import sqrt, pow, hypot


class HandDetector(): 

    def __init__(self, mode = False, maxHands = 2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)  
        self.mpDraw = mp.solutions.drawing_utils

      

    def findHands(self, img, draw = True): 
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB) # processes the rgb image

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks: 
                if draw: 
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img




    def findPosition(self, img, handNo = 0, draw=True): 
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark): 
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([cx, cy]) # appends the positions of the lms
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        return lmList
    



    def findDistance(x1=0,y1=0,x2=0,y2=0): #returns distance between points in 2D plane
        return hypot((x2-x1), (y2-y1))
          





def main():
    frameWidth,frameHeight = 640, 480
    cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    pTime = 0
    cTime = 0
    fpsStr = "FPS: "

    detector = HandDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmlist = detector.findPosition(img)

        if len(lmlist) != 0:
           print(lmlist[4])  

    
        cTime = time.time() #frame rate
        fps = 1/(cTime-pTime)
        pTime = cTime


        cv2.putText(img, fpsStr + str(int(fps)), (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 1)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break


if __name__ == '__main__':
    main()


