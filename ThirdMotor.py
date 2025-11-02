#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import Motor,TouchSensor
from pybricks.parameters import Stop, Direction
from pybricks.tools import wait

##--##--##--## ROBO CONSTANTS ##--##--## 
import RoboConstants as RC

##--##--##--## CODE CONSTANTS ##--##--##--##
import CodeCostants as CC

##--##--##--## ROBO SET UP ##--##--## 
ThirdMotor = Motor( RC.Motors['third'],positive_direction = Direction.COUNTERCLOCKWISE )

##--##--##--## func ##--##--##--##
def Move_gate(direct):
    # this func does both open & close the gate
    if direct.lower() == "open":
        flag = 1
    elif direct.lower() == "close":
        flag = -1
    else:
        print("incorrect direction input to gate moving func")

    ThirdMotor.run_angle(
        CC.GateSpeed,
        CC.GateAngle * flag,
        then=Stop.HOLD,
        wait=True
    )

##--##--##--## cycle ##--##--##--##
Move_gate("close")
wait(100)
Move_gate("open")