#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import Motor,TouchSensor
from pybricks.tools import StopWatch

##--##--##--## ROBO CONSTANTS ##--##--## 
import RoboConstants as RC

##--##--##--## ROBO SET UP ##--##--## 
ThirdMotor = Motor( RC.Motors['third'],positive_direction = Direction.COUNTERCLOCKWISE )

FrontBtn = TouchSensor( RC.Buttons['front'] )

##--##--##--## func ##--##--##--##
def Move_gate(direct):
    # this func does both open & close the gate
    if direct.lower() == "open":
        flag = -1
    elif direct.lower() == "close":
        flag = 1
    else:
        print("incorrect direction input to gate moving func")

    SortingMotor.run_angle(
        CC.GateSpeed,
        CC.GateAngle * flag,
        then=Stop.HOLD,
        wait=True
    )

##--##--##--## cycle ##--##--##--##
Move_gate("close")
wait(10)
Move_gate("open")