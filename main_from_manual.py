#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor
from pybricks.parameters import Direction
from pybricks.tools import wait, StopWatch, DataLog

##--##--##--## ROBO CONSTANTS ##--##--## 
import constants_robo as RC

##--##--##--## CODE CONSTANTS ##--##--##--##
import constants_code as CC


## robo setup
MainMotor = Motor( RC.Motors['main'],positive_direction = Direction.CLOCKWISE )
ArmMotor = Motor( RC.Motors['arm'],positive_direction = Direction.CLOCKWISE )

# just in case - however it is most likely redundant
ArmMotor.reset_angle(0)
MainMotor.reset_angle(0)

Motors = [MainMotor,ArmMotor]

btn = TouchSensor(RC.Buttons['1'])
Ev3 = EV3Brick()

## variables setup
hodinky = StopWatch()
hodinky.reset()

safety_delay = CC.safety_delay
v = [[CC.Speed['Main'], CC.Speed['Arm']],
     [CC.Boost['Main'], CC.Boost['Arm']]
]


angles = CC.angles


hodinky.resume()
for i in angles:
    Ev3.speaker.beep()

    Motors[ i[1] ].run_target(
                    v[ i[2] ][ i[1] ], # speed - first coord carries boost values
                    i[0]
    )

    wait(safety_delay)

# End data
Ev3.speaker.beep()
hodinky.pause()
t = hodinky.time()

print("End\n time to spare: "+str(90-t/1000)
       + '\n avrg time per piece: '+ str(round(t/(1000*8),2)))