# 3dilek - objet z venci a tim otocit, pak nabrat do pravy  a pritahnout
#

#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

##--##--##--## ROBO CONSTANTS ##--##--## 
import constants_robo as RC

##--##--##--## CODE CONSTANTS ##--##--##--##
import constants_code as CC


## robo setup
MainMotor = Motor( RC.Motors['main'],positive_direction = Direction.CLOCKWISE )
ArmMotor = Motor( RC.Motors['arm'],positive_direction = Direction.CLOCKWISE )
btn = TouchSensor(RC.Buttons['1'])
Ev3 = EV3Brick()

speed = CC.RotationSpeed


# part I
sect_i = 1

def _90deg():
    MainMotor.run_angle(speed,100)

#shorten 1, dont care about inaccuracy

while sect_i < 5:
    print( CC.Rot_vals[0][sect_i] )

    if sect_i ==1:
        _90deg()
    MainMotor.run_angle(speed, CC.Rot_vals[0][sect_i] )

    if sect_i % 2:
        Ev3.speaker.beep()

    if sect_i == 4:
      
        Ev3.speaker.play_notes(['C4/4', 'E4/4', 'D4/4'], tempo=120)

    
    ArmMotor.run_angle(360, -1 * CC.Arm_dists[0][sect_i])
    if sect_i != 4:
        ArmMotor.run_angle(360, CC.Arm_dists[0][sect_i +1])
    sect_i += 1

    waiting = input('press to continue:')

input('stop')

# part II
sect_i = 1

while sect_i < 5:
    MainMotor.run_angle(speed, CC.Rot_vals[1][sect_i] )

    ArmMotor.run_angle(360, CC.Arm_dists[1][sect_i])
    
    if sect_i % 2==0:
        Ev3.speaker.beep()

    
    ArmMotor.run_angle(360, -1 * CC.Arm_dists[1][sect_i])
    sect_i += 1
