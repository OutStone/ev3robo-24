#!/usr/bin/env pybricks-micropython
# pridat nastaveni pozice packy pres kostku pri pousteni
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
if True:


    Rotor = Motor( RC.Motors['rotor'],positive_direction = Direction.CLOCKWISE )

    Arm1 = Motor( RC.Motors['1'],positive_direction = Direction.CLOCKWISE )
    Arm2 = Motor( RC.Motors['2'],positive_direction = Direction.CLOCKWISE )


    Motors = [  [Rotor],
                [Arm1, Arm2]
    ]

    Btn_l = TouchSensor(RC.Buttons['l'])
    Btn_r = TouchSensor(RC.Buttons['r'])

    Btns = [ 
        Btn_l,
        Btn_r
    ]

    Ev3 = EV3Brick()

## variables setup
if True:
    hodinky = StopWatch()
    hodinky.reset()
    hodinky.resume()


    v = CC.v
    
    reached = [6, 6] 
    now_pressed = [False, False] 
    pres_time = [hodinky.time(), hodinky.time()] 
    btn_cooldown = 100
    
    while True:
        Motors[1][0].run(v["slow"][1]*8)
        Motors[1][1].run(v["slow"][1]*8)
        
        while reached[0] + reached[1] != 0:
            for i in [0,1]:
                if reached[i] == 0:
                    continue
                
                if hodinky.time() - pres_time[i] < btn_cooldown:
                    continue

                if Btns[i].pressed():
                    if not now_pressed[i]:
                        pres_time[i] = hodinky.time()
                        now_pressed[i] = True

                        reached[i] -= 1
                        if reached[i] == 0:
                            Motors[1][i].hold()
                else:
                    if now_pressed[i]: 
                        now_pressed[i] = False

            wait(CC.button_delay)

        a = input('empty = continue')
        if a != '':
            break