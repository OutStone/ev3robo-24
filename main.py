#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

##--##--##--## ROBO CONSTANTS ##--##--## 
from RoboConstants import Motors, Buttons, ColorSensor_port, InfraSensor_port, UlraSensor_port, Wheel_Diameter, Axle_Track

##--##--##--## CODE CONSTANTS ##--##--##--##
from CodeCostants import DriveSpeed, GameStage, SortingSpeed, SortAngle, WallDistance, linKoef, expKoef, DistanceAvrg, Values_in_Avrg

##--##--##--## ROBO SET UP ##--##--## 
Ev3 = EV3Brick()

# Motors
LeftMotor = Motor( Motors['left'],positive_direction = Direction.COUNTERCLOCKWISE )
RightMotor = Motor( Motors['right'],positive_direction = Direction.COUNTERCLOCKWISE )

robot = DriveBase( LeftMotor, RightMotor, Wheel_Diameter, Axle_Track )

# Sensors
FrontBtn =  TouchSensor( Buttons['front'] )
#InfraSensor = InfraredSensor( InfraSensor_port )
UlraSensor = UltrasonicSensor( UlraSensor_port )


##--##--##--## GAME LOOP ##--##--##--##
Ev3.speaker.beep()

while True:

    # stop the program detection
    if FrontBtn.pressed():
        break

    # Following wall with infrared sensor
    # dist = InfraSensor.distance()
    dist = UlraSensor.distance()
    error = WallDistance - dist/10 # dividing by 10 'cause ultrasonic sensor gives answer in mm -- delete the dividing when working with infraRed

    num = (error**expKoef) * linKoef

    if num > 100:
        num = 100

    lenght = len(DistanceAvrg)
    sum = 0

    if lenght == 0:
        DistanceAvrg.append(num)
        correction_Angle = num
    else:
        if lenght == Values_in_Avrg:
            DistanceAvrg.pop(0)
        DistanceAvrg.append(num)

        for i in DistanceAvrg:
            sum += i
        correction_Angle = sum/lenght

    
    print(error, num, correction_Angle)

    robot.drive(-1*DriveSpeed, correction_Angle)