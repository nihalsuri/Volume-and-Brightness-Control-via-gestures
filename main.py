from math import hypot
import HandTracking as ht
import cv2
import mediapipe as mp
import wmi
import time
from numpy import interp
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


frameWidth,frameHeight = 1280, 720
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
pTime = 0
cTime = 0
fpsStr = "FPS: "



# volume control 
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
minVol, maxVol = volume.GetVolumeRange()[0], volume.GetVolumeRange()[1] # setting the ranges 


# brightness control only for WINDOWS
maxBright = 100 # percentage [0-100] For changing thee screen 
minBright = 0 
c = wmi.WMI(namespace='wmi')
methods = c.WmiMonitorBrightnessMethods()[0]    
# methods.WmiSetBrightness(brightness, 0)



detectorHand = ht.HandDetector(detectionCon=0.8) # object for volume control 

while True:
    success, img = cap.read()
    img = detectorHand.findHands(img)
    lmlist = detectorHand.findPosition(img, draw=False)

    if len(lmlist) != 0: # print only if list is non-zero
        x1, y1 = lmlist[8] # index tip, volume Control
        x2, y2 = lmlist[4] # thumb tip
        x3, y3 = lmlist[20] # pinky tip



        # print("Index Tip: ", x1, y1)
        # print("Pinky Tip: ", x3, y3)
        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x3, y3), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (0, 0, 255), 3) # line between two points for volume 
        cv2.line(img, (x3, y3), (x2, y2), (0, 69, 255), 3) # line between two points for brightness 

        center_x1, center_y1 = (x1 + x2)//2, (y1+y2)//2 # centre point of the line for volume 
        center_x2, center_y2 = (x2 + x3)//2, (y2+y3)//2 # centre point of the line for brightness 

        cv2.circle(img, (center_x1, center_y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (center_x2, center_y2), 10, (255, 0, 255), cv2.FILLED)


        length_1 = round(hypot(x2-x1, y2-y1), 2) # returns length between index and thumb 
        length_2 = round(hypot(x2-x3, y2-y3), 2) # returns length between index and pinky
       # print(length_2) 

        # Index to Thumb Range 25 -> 250
        # Pinky yo Thumb Range 15 -> 440
        # Audio Range -65 -> 0

        #volume control
        vol_set = interp(length_1, [15, 250], [minVol, maxVol]) # thresholding  
        volumeBar_set = interp(length_1, [15, 250], [250, 50]) # volume bar thresholding 
        volumePercent = interp(length_1, [15, 250], [0, 100])

        volume.SetMasterVolumeLevel(vol_set, None)

        #brightness control 
        bright_set = interp(length_2, [15, 440], [minBright, maxBright]) 
        brightBar_set = interp(length_2, [15, 440], [500, 300]) # brightness bar thresholding 

        methods.WmiSetBrightness(bright_set, 0)




        #distance between landmarks
        cv2.putText(img, "dist(Index->Thumb): " + str(length_1), (800,30), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0 ), 1)
        cv2.putText(img, "dist(Pinky->Thumb): " + str(length_2), (800,60), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0 ), 1)

        #volume Bar
        cv2.rectangle(img, (30,250), (60, 50), (255, 0, 255), 5)
        cv2.rectangle(img, (30,250), (60, int(volumeBar_set)), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, "Vol: " + str(round(volumePercent, 2)) + "%" , (20, 280), cv2.FONT_ITALIC, 1, (255, 0, 200), 2)

        #brightness Bar 
        cv2.rectangle(img, (30,500), (60, 300), (0, 140, 255), 5)
        cv2.rectangle(img, (30,500), (60, int(brightBar_set)), (0, 140, 255), cv2.FILLED)
        cv2.putText(img, "Brightness: " + str(round(bright_set, 2)) + "%" , (20, 550), cv2.FONT_ITALIC, 1, (255, 140, 200), 2)


        if length_1 < 25:  
            cv2.circle(img, (center_x1, center_y1), 10, (0, 255, 0), cv2.FILLED)
        if length_2 < 15: 
            cv2.circle(img, (center_x2, center_y2), 10, (0, 255, 0), cv2.FILLED)
        
        


    
    cTime = time.time() #frame rate
    fps = 1/(cTime-pTime)
    pTime = cTime


    cv2.putText(img, fpsStr + str(int(fps)), (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 1)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break