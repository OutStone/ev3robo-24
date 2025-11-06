#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase

##--##--##--## DATA LOG ##--##--## 
log = ""

##--##--##--## ROBO CONSTANTS ##--##--## 
import RoboConstants as RC

##--##--##--## CODE CONSTANTS ##--##--##--##
import CodeCostants as CC

##--##--##--## ROBO SET UP ##--##--##
if True:
    Ev3 = EV3Brick()

    # Motors
    LeftMotor = Motor( RC.Motors['left'],positive_direction = Direction.CLOCKWISE )
    RightMotor = Motor( RC.Motors['right'],positive_direction = Direction.CLOCKWISE )

    # Sensors
    ColorSensor = ColorSensor( RC.ColorSensor_port )
    UlraSensor = UltrasonicSensor( RC.UlraSensor_port )

    FrontBtn = TouchSensor( RC.Buttons['front'] )
    SideBtn = TouchSensor( RC.Buttons['side'] )

##--##--##--## Driving Funcions ##--##--##--##
def Follow_Color():
    global log
    Color_now = ColorSensor.color()
    log += str(Color_now) + "     "
    if Color_now == Color.BLACK: # now it wants to find white => turning left
        RightMotor.run(CC.RotationSpeed*(1-CC.black_koef))
        LeftMotor.run(CC.RotationSpeed *(1+CC.black_koef))
        
    elif Color_now == Color.WHITE: # now it wants to find black => turning right
        RightMotor.run(CC.RotationSpeed*(1+CC.white_koef))
        LeftMotor.run(CC.RotationSpeed *(1-CC.white_koef))

    else: # this is the same as for white, but it should not happen so better make a note in game log
        log += "\033[93m LACK OF LIGHT:\033[00m " # in Yellow
        RightMotor.run(CC.RotationSpeed*(1+CC.white_koef))
        LeftMotor.run(CC.RotationSpeed *(1-CC.white_koef))
    log += str(Color_now) + "     "

def Stop_Dist(target):
    global log
    dist = UlraSensor.distance() + CC.DistanceSensor_Offset['backwards']
    log += str(dist) + "     "
    if dist >= CC.UltraSensorMax:
        print("Ultra reporting max value")
    elif dist >= target:
        LeftMotor.stop()
        RightMotor.stop()
        return True
    
    return False

##--##--##--## GAME LOOP ##--##--##--##
End = False
Reset = False
Changed = False
CC.DrivingStage = 1
while not End:
        if not Reset:
            Follow_Color()
            Reset = Stop_Dist(CC.StageValues[ CC.DrivingStage ]) # if I reached the target it returns True => next stage will activite
            print(log)
            log = ""
        else:
            if not Changed:
                W = input("     koefWhite: ")
                if not W == "":
                    CC.white_koef = float(W)
                B = input("     koefBlack: ")
                if not B == "":
                    CC.black_koef = float(B)
                Changed = True
            if SideBtn.pressed():
                Reset = False
                Changed = False
            if FrontBtn.pressed():
                End = True


print(
"""white_koef =""",CC.white_koef,"""
black_koef =""",CC.black_koef)