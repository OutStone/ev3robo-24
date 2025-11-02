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

##--##--##--## Driving Funcions ##--##--##--##
def Follow_Color():
    global log
    Color_now = ColorSensor.color()
    log += str(Color_now) + "     "
    if Color_now == Color.BLACK: # now it wants to find white => turning left
        RightMotor.run(CC.DriveSpeed*(1-CC.line_koef))
        LeftMotor.run(CC.DriveSpeed *(1+CC.line_koef))
    elif Color_now == Color.WHITE: # now it wants to find black => turning right
        RightMotor.run(CC.DriveSpeed*(1+CC.line_koef))
        LeftMotor.run(CC.DriveSpeed *(1-CC.line_koef))
    else: # this is the same as for white, but it should not happen so better make a note in game log
        print("LACK OF LIGHT:", Color_now)
        RightMotor.run(CC.DriveSpeed*(1+CC.line_koef))
        LeftMotor.run(CC.DriveSpeed *(1-CC.line_koef))


def Stop_Dist(target):
    global log
    dist = UlraSensor.distance() + CC.DistanceSensor_Offset['backwards']
    log += str(dist) + "     "
    if dist >= CC.UltraSensorMax:
        print("Ultra reporting max value")
        return True
    elif dist >= target:
        return True
    
    return False

##--##--##--## GAME LOOP ##--##--##--##
End = False
while not End:
        Follow_Color()
        End = Stop_Dist(CC.StageValues[ CC.DrivingStage ]) # if I reached the target it returns True => next stage will activite
        print(log)
        log = ""


LeftMotor.stop()
RightMotor.stop()