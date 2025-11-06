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

CC.DrivingStage = 1
base = 1.001
color_streak = 0 # negative value ...  white color  x   positive value ... black color

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
    global log,color_streak,base
    Color_now = ColorSensor.color()
    log += str(Color_now) + "     "
    
    if Color_now == Color.BLACK: # now it wants to find white => turning left
        if color_streak < 0:
            color_streak = 0
        else:
             color_streak += 1
        K = CC.black_koef*(base**(abs(color_streak)))
        RightMotor.run(CC.RotationSpeed*(1-K))
        LeftMotor.run(CC.RotationSpeed *(1+K))
        
    elif Color_now == Color.WHITE: # now it wants to find black => turning right
        if color_streak > 0:
            color_streak = 0
        else:
             color_streak -= 1
        K = CC.white_koef*(base**(abs(color_streak)))
        RightMotor.run(CC.RotationSpeed*(1+K))
        LeftMotor.run(CC.RotationSpeed *(1-K))

    else: # this is the same as for white, but it should not happen so better make a note in game log
        log += "\033[93m LACK OF LIGHT:\033[00m " # in Yellow
        
        if color_streak > 0:
            color_streak = 0
        else:
             color_streak -= 1
        K = CC.white_koef*(base**(abs(color_streak)))
        RightMotor.run(CC.RotationSpeed*(1+K))
        LeftMotor.run(CC.RotationSpeed *(1-K))
    log += str(Color_now) + "     " + str(K) + "     "

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

while not End:
        if not Reset:
            Follow_Color()
            Reset = Stop_Dist(CC.StageValues[ CC.DrivingStage ]) # if I reached the target it returns True => next stage will activite
            print(log)
            log = ""
        else:
            # adjusting values of koeficients
            if not Changed:
                W = input("     koefWhite: ")
                if not W == "":
                    CC.white_koef = float(W)
                B = input("     koefBlack: ")
                if not B == "":
                    CC.black_koef = float(B)
                X = input("     base: ")
                if not X == "":
                             base = float(X)
                Changed = True

            # running again or stopping the program
            if SideBtn.pressed():
                Reset = False
                Changed = False
            if FrontBtn.pressed():
                End = True


print(
"""white_koef =""",CC.white_koef,"""
black_koef =""",CC.black_koef,"""
base =""",base)