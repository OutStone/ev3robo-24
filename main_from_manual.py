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
Rotor = Motor( RC.Motors['rotor'],positive_direction = Direction.CLOCKWISE )

Arm1 = Motor( RC.Motors['1'],positive_direction = Direction.CLOCKWISE )
Arm2 = Motor( RC.Motors['2'],positive_direction = Direction.CLOCKWISE )

Motors = [  [Rotor],
            [Arm1, Arm2]
]

Ev3 = EV3Brick()

## variables setup
hodinky = StopWatch()
hodinky.reset()


v = {
    "quick" : [CC.Quick['rotor'],CC.Quick['arm']],
    "slow" : [CC.Slow['rotor'],CC.Slow['arm']]
}


Move_log = CC.Move_log


hodinky.resume()
for cmd in Move_log:
    Ev3.speaker.beep()

    i = cmd[1]
    if len(Motors[ i ]) > 1:
        Motors[i][0].run_target(
                    v[ cmd[2] ][ cmd[1] ], # speed - first coord carries boost values
                    cmd[0],
                    wait=False
        )
    Motors[i][ -1 ].run_target(         # running the first motor from the end, there are either two or just one motor.  for two it now runs the secodn one (the first one is already running asynchonously) 
                    v[ cmd[2] ][ cmd[1] ], # speed - first coord carries boost values
                    cmd[0]
    )

    wait(CC.safety_delay)

# End data
Ev3.speaker.beep()
hodinky.pause()
t = hodinky.time()

print("End",
      '\n time to spare: '+str(90-t/1000),
      '\n avrg time per piece: '+ str(round(t/(1000*8),2)),
       '\n sum of all waiting: ' + str( len(Move_log) * CC.safety_delay)
)