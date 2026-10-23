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
ArmMotor.reset_angle(CC.Arm_start)

Motors = [MainMotor,ArmMotor]

btn = TouchSensor(RC.Buttons['1'])
Ev3 = EV3Brick()


## variables setup
hodinky = StopWatch()
hodinky.reset()

transl = {
    0 : 'Main',
    1 : 'Arm'
}

safety_delay = CC.safety_delay
Times = [[],[]]
last_time = 0

angles = []

v = [[CC.Speed['Main'], CC.Speed['Arm']],
     [CC.Boost['Main'], CC.Boost['Arm']]
]


# begging_angle = int(input('angle on which the arm extender is starting:'))
# ArmMotor.reset_angle(begging_angle)

stop = ''
while True:
    wait(safety_delay)
    Ev3.speaker.beep()
    # input categorisation
    if True:
        # stop can carry a value from breaking
        #            - we can omit breaking and go straight forward to new movement  
        if not stop.lower() in ['w','s','a','d']:
            d = input('(ws - ad - x):')
            if d.lower() == "x":
                break
        else:
            d = stop
            print('going straight to new move') # TODO: this will go away

        # Boost or normal speed 
        speed_type = 0
        if d.lower() != d:
            speed_type = 1
        # Reverse
        k = 1
        if d in ['s','d']:
            k = -1

        # which motor should run?
        i = 0
        if d in ['w','s']:
            i = 1

    # run  
    hodinky.resume()
    Motors[i].run(v[speed_type][i] * k)

    stop = input('brake:')
    Motors[i].hold()
    hodinky.pause()

    t = hodinky.time()
    Ev3.speaker.beep()

    # data management
    index = len(angles)
    Times[i].append([
         t-last_time,
         index
    ])
    angles.append([
         Motors[i].angle(),
         i,
         speed_type
    ])

    print('                    angle: '+ str(round(angles[-1][0]*2,-2)/2) + '; T= ' + str(round(t,-2)) +'; dT= ' +  str(round(Times[i][-1][0], -2)))
    last_time = t

print("End\n time to spare: "+str(90-t/1000),
       '\nangles=',angles,
       '\nRotor_times=',Times[0],
       '\nArm_times=',Times[1])