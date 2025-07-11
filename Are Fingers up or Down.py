#Import the necessary Packages and scritps for this software to run (Added speak in
#there too as an easer egg)
import cv2
from collections import Counter
from module import findnameoflandmark,findpostion
import mediapipe as mp
from hand_count import*

from gpiozero import Servo
from time import sleep
import RPi.GPIO as GPIO
import time



#Relay Control code

handsModule = mp.solutions.hands
# Set the GPIO pin numbers
PIN_RELAY_1 = 12 # GPIO12
#PIN_RELAY_2 = 16 # GPIO16
PIN_RELAY_3 = 20 # GPIO20
PIN_RELAY_4 = 21 # GPIO21

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Setup the GPIO pins as outputs
GPIO.setup(PIN_RELAY_1, GPIO.OUT)
#GPIO.setup(PIN_RELAY_2, GPIO.OUT)
GPIO.setup(PIN_RELAY_3, GPIO.OUT)
GPIO.setup(PIN_RELAY_4, GPIO.OUT)


mod = handsModule.Hands()


#Uses CV2 Functionality to create a Video stream and add some values + variables
cap = cv2.VideoCapture(0)
tip=[8,12,16,20]
tipname=[8,12,16,20]
fingers=[]
finger=[]

#Create an infinite loop which will produce the live feed to our desktop and that will search for hands
while True:
     ret, frame = cap.read() 
     #Unedit the below line if your live feed is produced upsidedown
     #flipped = cv2.flip(frame, flipCode = -1)
     
     #Determines the frame size, 640 x 480 offers a nice balance between speed and accurate identification
     frame1 = cv2.resize(frame, (640, 480))
     ret, frame = cap.read()
     hand_count = count_hands(frame)
     if hand_count==1:
         #Below is used to determine location of the joints of the fingers
         a=findpostion(frame1)
         b=findnameoflandmark(frame1)

         #Below is a series of If statement that will determine if a finger is up or down and
         #then will print the details to the console
         if len(b and a)!=0:
            fingers_count=[]
            if a[0][1:] < a[4][1:]:
               finger.append(1)
               #print (b[4])

            else:
               finger.append(0)

            fingers=[]
            for id in range(0,4):
                if a[tip[id]][2:] < a[tip[id]-2][2:]:
                   fingers_count.append(b[tipname[id]])

                   #fingers.append(1)

                else:
                   #fingers.append(0)
                   fingers_count.append(0)
         #Below will print to the terminal the number of fingers that are up or down
#             print(fingers_count)
            if fingers_count==[0,0,0,0]:
                GPIO.output(PIN_RELAY_3, True)
                print("LED1 Off")   
            if fingers_count==['INDEX FINGER TIP',0,0,0]:
                GPIO.output(PIN_RELAY_1, False)
                print("LED2 on")
            if fingers_count==['INDEX FINGER TIP', 'MIDDLE FINGER TIP', 'RING FINGER TIP', 'PINKY TIP']:
                GPIO.output(PIN_RELAY_3, False)
                print("LED1 on")
            if fingers_count==['INDEX FINGER TIP',0,0,'PINKY TIP']:
                GPIO.output(PIN_RELAY_4, False)
                print("Motor On")
            if fingers_count==['INDEX FINGER TIP', 'MIDDLE FINGER TIP', 'RING FINGER TIP',0]:
                GPIO.output(PIN_RELAY_1, True)
                print("LED2 Off")
            if fingers_count==['INDEX FINGER TIP', 'MIDDLE FINGER TIP',0,0]:
                GPIO.output(PIN_RELAY_4, True)
                print("Motor Off")

         #Below shows the current frame to the desktop
         cv2.imshow("Frame", frame1);
         key = cv2.waitKey(1) & 0xFF
         
     else:
         ret, frame = cap.read()
         hand_count = count_hands(frame)
         if hand_count == 2:
             print("place properly")