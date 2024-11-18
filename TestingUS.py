#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

##--##--##--## ROBO CONSTANTS ##--##--## 
from RoboConstants.py
# TODO: test if I can just import the file without specifing the variables to be imported
RUN = True

##--##--##--## CODE CONSTANTS ##--##--##--##
import CodeConstants

##--##--##--## ROBO SET UP ##--##--## 
Ev3 = EV3Brick()

# Motors
LeftMotor = Motor( Motors['left'],positive_direction = Direction.COUNTERCLOCKWISE )
RightMotor = Motor( Motors['right'],positive_direction = Direction.COUNTERCLOCKWISE )

robot = DriveBase( LeftMotor, RightMotor, Wheel_Diameter, Axle_Track )

# Sensors
FrontBtn =  TouchSensor( Buttons['front'] )
UlraSensor = UltrasonicSensor( UlraSensor_port )


##--##--##--## GAME LOOP ##--##--##--##
Ev3.speaker.beep()

 # while pressing the button this program can run multiple game cycles
 # - this ensures that anything linked to pressing button will be executed just once
btnDown = False
ingoreBtns = False

while RUN:

    # stop the program detection
    if FrontBtn.pressed():
        
        if RUN and not btnDown:
            robo.stop()
            RUN = False
        elif not btnDown:
            RUN = True
        
        Ev3.speaker.beep()
        btnDown = True
    else:
        btnDown = False


    if RUN:
        # Following wall with infrared sensor
        dist = InfraSensor.distance()
        error = WallDistance - dist
        print(error*koeficient)

        robo.drive(DriveSpeed, error * koeficient)
    elif not ingoreBtns:
        pressed = Ev3.buttons.pressed()

        if len(pressed) != 0:
            print(pressed)
            if Button.DOWN in pressed:
                print('decreasing by 10%')
                koeficient *= 0.9

            elif Button.Up in pressed:
                print('increasing by 10%')
                koeficient *= 1.1

            elif Button.RIGHT in pressed:
                print('decreasing by a half')
                koeficient *= 0.5

            elif Button.LEFT in pressed:
                print('increasing by a half')
                koeficient *= 2

            print("new koeficient=" + str(koeficient))
            ingoreBtns = True