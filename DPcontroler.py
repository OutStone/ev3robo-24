#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

##--##--##--## ROBO CONSTANTS ##--##--## 
import RoboConstants as RC

##--##--##--## CODE CONSTANTS ##--##--##--##
import CodeCostants as CC

##--##--##--## ROBO SET UP ##--##--## 
Ev3 = EV3Brick()

# Motors
LeftMotor = Motor( RC.Motors['left'],positive_direction = Direction.COUNTERCLOCKWISE )
RightMotor = Motor( RC.Motors['right'],positive_direction = Direction.COUNTERCLOCKWISE )

# Sensors
FrontBtn = TouchSensor( RC.Buttons['front'] )
UlraSensor = UltrasonicSensor( RC.UlraSensor_port )

##--##--##--## Driving Funcions ##--##--##--##

def Follow_Ultra(target):
        global integral, previous_error
        dist = UlraSensor.distance()/10

        print(round(dist, 3))

        error = target - dist

        integral += error
        derivative = error - previous_error

        correction = CC.Kp2 * error + CC.Ki2 * integral + CC.Kd2 * derivative
        previous_error = error

        left_speed = (CC.DriveSpeed + correction) *-1  # INVERTED!!
        right_speed = (CC.DriveSpeed - correction) *-1 # INVERTED!!

        RightMotor.run(left_speed)
        LeftMotor.run(right_speed)

##--##--##--## GAME LOOP ##--##--##--##

previous_error = 0
integral = 0

Cycle_Clock = StopWatch()

LoopTime = 20


while True:
    # stop the program detection
    if FrontBtn.pressed():
        LeftMotor.stop()
        RightMotor.stop()

        Ev3.speaker.beep()
        break
        

    Follow_Ultra( CC.StageValues[5] )

    # making a constant time drive loop 
    if Cycle_Clock.time() < LoopTime:
        wait(LoopTime - Cycle_Clock.time())
    else:
        print('\033Err: cycle took to long!\033') # printing in red color
        print(Cycle_Clock.time())
    
    Cycle_Clock.reset()