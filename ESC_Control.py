# This program will let you test your ESC and brushless motor.
# Make sure your battery is not connected if you are going to calibrate it at first.
# Since you are testing your motor, I hope you don't have your propeller attached to it otherwise you are in trouble my friend...?
# This program is made by AGT @instructable.com. DO NOT REPUBLISH THIS PROGRAM... actually the program itself is harmful                                             pssst Its not, its safe.

import os     #importing os library so as to communicate with the system
import time   #importing time library to make Rpi wait because its too impatient 
os.system ("sudo pigpiod") #Launching GPIO library
time.sleep(1) # As i said it is too impatient and so if this delay is removed you will get an error
import pigpio #importing GPIO library
#Connect the ESC in this GPIO pin 
from getch import getch
pi = pigpio.pi();
pi.set_servo_pulsewidth(ESC, 0) 

 #change this if your ESC's min value is different or leave it be
print ("For first time launch, select calibrate")
print ("Type the exact word for the function you want")
print ("calibrate OR manual OR control OR arm OR stop")
class ESC():
    def __init__(self,pin,max_value = 2000,min_value = 700,calibrated=False ):
        self.pin=pin
        self.max_value=max_value
        self.min_value=min_value
        self.calibrated=calibrated
        if calibrated == False:
            self.calibrate()
    def manual_drive(self): #You will use this function to program your ESC if required
        print "You have selected manual option so give a value between 0 and {0} type 'stop' to exit".format(self.max_value)    
        while True:
            inp = raw_input()
            if inp == "stop":
                self.stop()
                break
            else:
                pi.set_servo_pulsewidth(self.pin,inp)
                    
    def calibrate(self):   #This is the auto calibration procedure of a normal ESC
        pi.set_servo_pulsewidth(self.pin, 0)
        print("Disconnect the battery and press enter")
        time.sleep(1)
        inp = raw_input()
        if inp == '':
            pi.set_servo_pulsewidth(self.pin, self.max_value)
            print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
            inp = raw_input()
            if inp == '':            
                pi.set_servo_pulsewidth(self.pin, self.min_value)
                print "Wierd eh! Special tone"
                time.sleep(7)
                print "Wait for it ...."
                time.sleep (5)
                print "Im working on it, DONT WORRY JUST WAIT....."
                pi.set_servo_pulsewidth(self.pin, 0)
                time.sleep(2)
                print "Arming ESC now..."
                pi.set_servo_pulsewidth(self.pin, self.min_value)
                self.calibrated=True 
                self.arm()
                print "ESC Calibrated and Armed"
                # You can change this to any other function you want
                
    def control(self): 
        print "I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'"
        time.sleep(1)
        speed = 1500    # change your speed if you want to.... it should be between 700 - 2000
        print "Controls - a to decrease speed & d to increase speed OR q to decrease a lot of speed & e to increase a lot of speed"
        while True:
            pi.set_servo_pulsewidth(ESC, speed)
            inp = getch()
            
            if inp == "q":
                speed -= 100    # decrementing the speed like hell
                print "speed = %d" % speed
            elif inp == "e":    
                speed += 100    # incrementing the speed like hell
                print "speed = %d" % speed
            elif inp == "d":
                speed += 10     # incrementing the speed 
                print "speed = %d" % speed
            elif inp == "a":
                speed -= 10     # decrementing the speed
                print "speed = %d" % speed
            elif inp == "y":
                self.stop()          #going for the stop function
                break
            else:
                print "WHAT DID I SAID!! Press a,q,d or e"
            
    def arm(self): #This is the arming procedure of an ESC 
        pi.set_servo_pulsewidth(self.pin, 0)
        time.sleep(1)
        pi.set_servo_pulsewidth(self.pin, self.max_value)
        time.sleep(1)
        pi.set_servo_pulsewidth(self.pin, self.min_value)
        time.sleep(1)
        self.control() 
        
    def stop(self): #This will stop every action your Pi is performing for ESC ofcourse.
        pi.set_servo_pulsewidth(self.pin, 0)
        pi.stop()
if __name__=="__main__":
    Test=ESC(4)
    Test.control()

#This is the start of the program actually, to start the function it needs to be initialized before calling... stupid python.    