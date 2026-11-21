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

    Time_log = [[],[]]
    t = 0
    time_last = 0

    Move_log = []

    v = {
        "quick" : [CC.Quick['rotor'],CC.Quick['arm']],
        "slow" : [CC.Slow['rotor'],CC.Slow['arm']]
    }
    
    Move_log = CC.Move_log
    record_index = 0

## movement funcs
def checkpoints(n):
    global hodinky, Motors, v
    dir = 1 if n < 0 else -1
    n = abs(n)
    reached = [n, n] 
    now_pressed = [False, False] 
    
    Motors[1][0].run(v["quick"][1] * dir) # TODO: dir is not in saved values
    Motors[1][1].run(v["quick"][1] * dir)
            
    while reached[0] + reached[1] != 0:
        for i in [0,1]:
            if reached[i] == 0:
                continue
                
            if Btns[i].pressed():
                if not now_pressed[i]:
                    now_pressed[i] = True

                    reached[i] -= 1
                    if reached[i] == 0:
                        Motors[1][i].hold()
            else:
                if now_pressed[i]: 
                    now_pressed[i] = False
        
        wait(CC.button_delay)
def recorded_angle(cmd):
    global hodinky, Motors, v
    i = cmd[2]

    if len(Motors[ i ]) > 1:
        Motors[i][0].run_target(
                    v[ cmd[3] ][ cmd[2] ], # speed - first coord carries boost values
                    cmd[1],
                    wait=False
        )
    Motors[i][ -1 ].run_target(         # running the first motor from the end, there are either two or just one motor.  for two it now runs the secodn one (the first one is already running asynchonously) 
                    v[ cmd[3] ][ cmd[2] ], # speed - first coord carries boost values
                    cmd[1]
    )


hodinky.resume()
for cmd in Move_log:
    Ev3.speaker.beep()

    if cmd[0] == 'A':
        recorded_angle(cmd)
    elif cmd[0] == 'P':
        checkpoints(cmd[1])

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