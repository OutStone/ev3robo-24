#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import Motor,TouchSensor
from pybricks.tools import StopWatch

##--##--##--## ROBO CONSTANTS ##--##--## 
import RoboConstants as RC

##--##--##--## ROBO SET UP ##--##--## 
SortingMotor = Motor( RC.Motors['sort'],positive_direction = Direction.COUNTERCLOCKWISE )

FrontBtn = TouchSensor( RC.Buttons['front'] )

Clock = StopWatch()
switch = False

##--##--##--## func ##--##--##--##
def test(Reverse):
    Clock.reset()

    if not Reverse:
        SortingMotor.run_angle(
            CC.SortSpeed,
            CC.SortAngle['red'],
            then=Stop.HOLD,
            wait=True
        )
        print(Clock.time())
        Clock.reset()
        SortingMotor.run_angle(
            CC.SortSpeed,
            CC.SortAngle['red'] * -1,
            then=Stop.HOLD,
            wait=True
        )
    else:
        SortingMotor.run_angle(
            CC.SortSpeed,
            CC.SortAngle['blue'],
            then=Stop.HOLD,
            wait=True
        )
        print(Clock.time())
        Clock.reset()
        SortingMotor.run_angle(
            CC.SortSpeed,
            CC.SortAngle['blue'] * -1,
            then=Stop.HOLD,
            wait=True
        )
    print(Clock.time())

##--##--##--## cycle ##--##--##--##
while True:
    if Clock.time() > 10 * 1000: # each 10 seconds
        test(switch)
        if switch:
            switch = False
        else:
            switch = True

    # break the loop
    if FrontBtn.pressed():
        break
