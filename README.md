# Volume-and-Brightness-Control-via-gestures
Using **OpenCV** and Googles **Mediapipe** ML Pipeline control volume and brightness of your laptop using hand gestures. 

# Implementation 
To control the audio on the system the **pycaw** library has been used and for the volume **wmi** has been used so this is meant to function only on a windows system and not linux or mac os. 

# Procedure
The distance in pixels is measured between the thumb and index finger for the volume and the ditance between the thumb and pinky finger decides the brightness of your system (the distance between your fingers is directly proportional to the brightness or volume). There is a volume and brightness bar on the left side of the window and the distance between your fingers is displayed on the window at the top-right corner. 

![dist](https://user-images.githubusercontent.com/37659632/124911423-050e5280-dfed-11eb-8990-68485ffffff8.PNG)


Above is an example of how it looks when the program is running. 

Try it out and I hope you have fun with it:)
