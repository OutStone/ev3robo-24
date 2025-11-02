#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import TouchSensor, ColorSensor

##--##--##--## ROBO CONSTANTS ##--##--## 
import RoboConstants as RC

##--##--##--## ROBO SET UP ##--##--##
ColorSensor = ColorSensor( RC.ColorSensor_port )
SideBtn = TouchSensor( RC.Buttons['side'] )

##--##--##--## GAME LOOP ##--##--##--##
while True:
    if SideBtn.pressed():
        print(ColorSensor.color())