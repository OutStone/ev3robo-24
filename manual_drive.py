#!/usr/bin/env pybricks-micropython
# TODO: 2D movement -> new key words (use numbers for better orient)
# upgrade the overwrite func - zbytecny
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

    Btn_l = 2#TouchSensor(RC.Buttons['l'])
    Btn_r = 1#TouchSensor(RC.Buttons['r'])

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
        "fast" : [CC.Fast['rotor'],CC.Fast['arm']],
        "quick" : [CC.Quick['rotor'],CC.Quick['arm']],
        "slow" : [CC.Slow['rotor'],CC.Slow['arm']]
    }
    
    Record_log = CC.Move_log
    record_index = 0

# helping funcs
def move_info(i):
    global time_last,t,Motors,Move_log,Time_log
    gap = '           '
    print(gap + 'angle: '+ str(round(Move_log[-1][1]*2,-2)/2))
    print(gap + '   T=  '+ str(round(t,-2)) +'; dT= ' +  str(round(Time_log[ i ][-1][0], -2)))
    if i == 1:
        print(gap + 'delta arm:', Motors[1][0].angle() - Motors[1][1].angle() )
    time_last = t

def reset():
    global Move_log,index,Time_log,time_last,record_index
    index = []
    Move_log = []
    Time_log = [[],[]]
    hodinky.reset()
    time_last = 0
    record_index = 0

    Motors[0][0].reset_angle(0)
    Motors[1][0].reset_angle(0)
    Motors[1][1].reset_angle(0)

    cls()
    print("     reset completed - list of moves is now empty")

def log():
    print("time to spare: "+str(90-t/1000),
        '\nMove_log=',Move_log,
        '\nRotor_times=',Time_log[0],
        '\nArm_times=',Time_log[1],
        '\n delta arm=', Motors[1][0].angle() - Motors[1][1].angle())

def cls():
    print("\x1b[2J\x1b[H", end="")

# movement funcs
def manual(i,speed_type, dir):
    global hodinky, Motors, v, Ev3
    global Time_log, Move_log, time_last, t, stop
    hodinky.resume()
            
    for m in Motors[i]:
        m.run(v[speed_type][i] * dir)

    # waiting for stop signal
    stop = input('brake or new cmd:')
    
    for m in Motors[i]:
        m.hold()
    
    hodinky.pause()

    t = hodinky.time()
    Ev3.speaker.beep()

    
    # DATA management
    index = len(Move_log)
    Time_log[i].append([
            t-time_last,
            index
    ])
    Move_log.append([
            'A',
            Motors[i][0].angle(),
            i,
            speed_type
    ])

    move_info(i)
    time_last = t


def checkpoints(n):
    global hodinky, Motors, v
    dir = 1 if n < 0 else -1
    n = abs(n)
    reached = [n, n] 
    now_pressed = [False, False] 

    # robo starts with already pressed btn -> target number is highered (this btn does not count)
    for i in [0,1]:
        if Btns[i].pressed():
            reached[i] += 1

    hodinky.resume()
    Motors[1][0].run(v["quick"][1] * dir)
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
    hodinky.pause()

# Following STORED COMMANDS
def recorded_angle(cmd):
    global hodinky, Motors, v
    i = cmd[2]

    hodinky.resume()
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
    hodinky.pause()


def from_record(index):
    global hodinky, Ev3, Motors, Time_log, Move_log, time_last, t

    if index >= len(Record_log):
        print('Whole Record was replayed')
        print(' - no command to do')
        return
    cmd = Record_log[index]

    # the MOVEMENT
    typ = cmd[0] 
    if typ == 'A':
        recorded_angle(cmd)
    if typ == 'P':
        checkpoints(cmd[1])

    # DATA management
    if True:
        t = hodinky.time()
        Time_log[cmd[2]].append([
                t-time_last,
                len(Move_log)
        ])
        Move_log.append([
                cmd[0],
                cmd[1],
                cmd[2],
                cmd[3]
        ])
    move_info(cmd[2])
    time_last = t

# other movement
def home():
    global Motors, v
    # arm half way home
    if True:
        Motors[1][0].run_target(
                    v[ "quick" ][ 1 ], # speed - first coord carries boost values
                    -570,
                    wait = False
        )
        Motors[1][ 1 ].run_target(         # running the first motor from the end, there are either two or just one motor.  for two it now runs the secodn one (the first one is already running asynchonously) 
                        v[ "quick" ][ 1 ], # speed - first coord carries boost values
                        -570
        )

    # rotor home
    Motors[0][ 0 ].run_target(         # running the first motor from the end, there are either two or just one motor.  for two it now runs the secodn one (the first one is already running asynchonously) 
                    v[ "quick" ][ 0 ], # speed - first coord carries boost values
                    0
    )

    # arm home
    if True:
        Motors[1][ 0 ].run_target(         # running the first motor from the end, there are either two or just one motor.  for two it now runs the secodn one (the first one is already running asynchonously) 
                        v[ "quick" ][ 0 ], # speed - first coord carries boost values
                        0,
                        wait = False
        )
        Motors[1][ 1 ].run_target(         # running the first motor from the end, there are either two or just one motor.  for two it now runs the secodn one (the first one is already running asynchonously) 
                        v[ "quick" ][ 0 ], # speed - first coord carries boost values
                        0
        )

stop = ''
while True:
    wait(CC.safety_delay)
    Ev3.speaker.beep()
    
    # INPUT
    if True:
        if not len(stop):
                d = input('(ws - ad - x):')
        else:
            d = stop
            stop = ''
            print('going straight to new move')

    # NO INPUT
    if d == '': continue

    # END of CYCLE
    if d.lower() == "x":
        break

    # HELP
    if d.lower() == 'h':
        cls()
        print("""list of keys/keywords in use:
   x    ... end run & drive back to start
                ( X ... omits the drive)
   h    ... print help
  log   ... show the trajectory log
   t    ... show the time management data
   ------------
 reset  ... deletes all the saved movement of this run
  pos   ... rewrite the robots pos in space
  home  ... drives back to start
   ------------
   l    ... execute previosly saved command
                (L ... no waiting after each move)
    + n > 0; = -1  ... number of commands to execute (-1 ... all commands)
    + i > 0; =  0  ... index of command where to start
  e,q   ... drives to the n-th checkpoint ahead (q is towards robo)
    + n > 0  ... number of checkpoints to pass
                DISSABLED
   ------------
  w,s   ... move arm
                 (W,S ... slowly)
  a,d   ... rotate arm
                (A,D ... slowly)
   ------------
   Driving speeds:
    "quick" =""", str(v["quick"]),"""
    "slow"  =""", str(v["slow"])
              )
        a = input('press to clear console:')
        cls()
        continue
    
    # RESET of MOVEMENT RECORDING
    if d.lower() == "reset": reset(); continue
        
    # LOG of TIME
    if d.lower() == 't':
        a_t = 0
        for time in Time_log[1]:
            a_t += time[0]

        print("     T:",time_last,
            "\n     a_t:",a_t,
            "\n     r_x",time_last-a_t,
            "\n     remain:", 90*1000 - time_last)
        continue
    
    # LOG of movement
    if d.lower() == 'log':
        cls()
        log()
        a = input('press to continue (console will be cleared)')
        cls()
        continue

    # REWRITE current POS
    if d.lower() == 'pos':
        x = int(input("arm:"))
        y = int(input("rotor:"))

        Motors[0][0].reset_angle(y)
        Motors[1][0].reset_angle(x)
        Motors[1][1].reset_angle(x)
        continue

    if d[0:4].lower() == 'edit':
        continue
        # while True:
        #     i = input("Which index you want to replace? (x to escape) : ") # TODO: check if it is in range
        #     if i == 'x':
        #         break
        #     i = int(i)
        #     print('i=',i,'- ',Record_log[i])
            
        #     ans = input('Is that correct? (y,n,x)')
        #     if ans == 'x':
        #         break # TODO: it drives home
        #     if ans == 'n':
        #         continue

        #     # new values
        #     res = []
        #     res.append(input('type of movement? (A / P):').upper())
        #     if res[0] == 'A':
        #         res.append(int(input('target angle?:'))) # TODO: add some dumb proofing for int func so it wont crash
        #         res.append(int(input('Arm or rotor? (1 / 0):'))) # TODO: just the same
        #         s = input('fast? (1/0)')
        #         if s == "1":
        #             res.append('quick')
        #         else:
        #             res.append('slow')
        #     elif res[0] == 'P':
        #         res.append(int(input('N of checkopoints?:'))) # TODO: add some dumb proofing for int func so it wont crash
        #         res.append(1)
        #         res.append('quick')
        #     else:
        #         print('bad input')
        #         continue
            
        #     print(res)
        #     ans = input('Is it ok? (*/n):')
        #     if ans == "n":
        #         continue
        #     else:
        #         Record_log[i] == res
        #         break
        # continue
    
    if d.lower() == "home":
        home()
        continue

    # sorting MOVEMENT vars
    if True:
            speed_type = 'quick'
            if d.lower() != d:
                speed_type = 'slow'
            # Reverse
            dir = 1
            if d[0].lower() in ['s','d','e']:
                dir = -1

            i = 0
            if d.lower() in ['s','w']:
                i = 1


    if d[0:1].lower() in ['e ','q ']:
        continue
        # berem dva znaky aby tam byla i mezera
        n = int(d[2:]) * dir # dvojtecka kdyby jich bylo vic jak 10
        checkpoints(n)
        
        t = hodinky.time()
        Time_log[1].append([
                t-time_last,
                len(Move_log)
        ])
        Move_log.append([
                'P',
                n,
                1,
                "quick"
        ])
        move_info(1)
        time_last = t
        continue


    # MOVEMENT - no mechanical stops
    if d.lower() in ['w','s','a','d']:
        manual(i,speed_type,dir)
        continue

    # MOVEMENT - from memory
    if d[0].lower() == 'l':
        ask_questions = (d[0].lower() == d[0]) # if "l" is lower case, then it asks questions

        l = d.split()
        if len(l) >= 2:
            n = int(l[1])

            if len(l) > 2:
                print("new memory index:",int(l[2]) + 1, "old memory index:", record_index + 1)
                record_index = int(l[2])
                
            if n < 0:
                n = len(Record_log) - record_index
        else:
            n = 1


        counter = 0
        while True:
            print('memory index:',record_index+1)
            from_record(record_index);   record_index += 1

            counter += 1
            if counter < n:
                if ask_questions:
                    stop = input('press for next move (key = end):')
                    if stop != '':
                        break
            else:
                break
        continue

if d.lower() == d:
    home()
cls()
print("End")
log()