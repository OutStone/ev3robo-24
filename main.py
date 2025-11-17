#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

##--##--##--## DATA LOG ##--##--## 
log = ""

##--##--##--## ROBO CONSTANTS ##--##--## 
import RoboConstants as RC

##--##--##--## CODE CONSTANTS ##--##--##--##
import CodeCostants as CC

##--##--##--## ROBO SET UP ##--##--##
if True:
    Ev3 = EV3Brick()

    # Motors
    DriveMotor = Motor( RC.Motors['drive'],positive_direction = Direction.COUNTERCLOCKWISE )
    ArmMotor = Motor( RC.Motors['arm'],positive_direction = Direction.COUNTERCLOCKWISE )
    #ThirdMotor = Motor( RC.Motors['third'],positive_direction = Direction.CLOCKWISE )


    # Sensors
    FrontBtn = TouchSensor( RC.Buttons['front'] )
    # SideBtn = TouchSensor( RC.Buttons['side'] )

    # ColorSensor = ColorSensor( RC.ColorSensor_port )

    # Gyro = GyroSensor( RC.Gyro_port )
    # InfraSensor = InfraredSensor( RC.InfraSensor_port )
    UlraSensor = UltrasonicSensor( RC.UlraSensor_port )

##--##--##--## Driving Funcions ##--##--##--##
def Stop_Dist(target):
    global log
    dist = UlraSensor.distance() + CC.DistanceSensor_Offset['backwards']
    log += str(dist) + "     "
    if dist >= CC.UltraSensorMax:
        print("\033[92m Ultra reporting max value \033[00m")
        return True
    elif dist >= target:
        return True
    
    return False

##--##--##--## working with tetris tiles ##--##--## 
def Move_Arm(direct,wait_for_it=True):
    # this func does back and forth movement with robot's arm
    if direct.lower() == "open":
        flag = -1
    elif direct.lower() == "close":
        flag = 1
    else:
        print("\033[91m incorrect direction input to gate moving func '{}'\033[00m ".format(direct))

    ArmMotor.run_target(
        CC.ArmSpeed,
        30000*flag
    )
    
##--##--##--## GAME LOOP ##--##--##--##
def END(msg):
    DriveMotor.stop()
    ArmMotor.stop()
    Ev3.speaker.beep()
    print("\033[92m", msg,"\033[00m")

if True: # set up of variables
    # driving
    End_of_stage = False # substitutes for a button press -> iniciates a robot turn

    Drive_Clock = StopWatch() # measuring robot turn angle in mechanical follow
    Drive_Clock.pause()
    Drive_Clock.reset()

    Game_Clock = StopWatch() # for game timing
    Game_Clock.pause()
    Game_Clock.reset()
    StageStartTime = 0
        
    Cycle_Clock = StopWatch() # for stable game loops
    Cycle_Clock.pause()
    Cycle_Clock.reset()

Start = False
while True:
    if FrontBtn.pressed():
        Start = True
    elif Start:
        # upon releasing the button (may take multiple game cycles) starts the game
        Game_Clock.resume()
        Cycle_Clock.resume()
        break



print("ARM MOVEMENT")
Move_Arm("close")
print("ARM MOVEMENT")
while False: # game loop
    
    if Game_Clock.time() >= CC.GameLenght:
        # the game time is up => robot should stop
        END("Time is up! - End")
        break

    # next stage triggered -> reseting before next game stage 
    if FrontBtn.pressed() or End_of_stage:
        # reseting driving clock
        Drive_Clock.pause()
        Drive_Clock.reset()

        # reseting variables
        CC.DrivingStage += 1
        End_of_stage = False

        # stoping the robot after movent
        DriveMotor.stop()
        ArmMotor.stop()

        # time logging
        print("         time:",Game_Clock.time()/1000,
              "  T"  +    str((   Game_Clock.time() - CC.GameLenght )/1000),
              "stage lenght:",(  Game_Clock.time() - StageStartTime )/1000)
        StageStartTime = Game_Clock.time()

        # forced stop
        if CC.DrivingStage == CC.EndRun_at:
            END("Forced End")
            break


    # driving stage logic
    if   CC.DrivingStage <= 9: # first 3 rows of tiles
        if CC.DrivingStage %3 == 1: # drives to next set of bricks
            print(1)
            DriveMotor.run(CC.RotationSpeed)
            End_of_stage = Stop_Dist(CC.StageValues[ CC.DrivingStage ] - CC.DistanceSensor_Offset["backwards"]) # if I reached the target it returns True => next stage will activite
        elif CC.DrivingStage %3 == 2:   # stacks tiles in storage
            print(2)
            Move_Arm("close")
            End_of_stage = True
        elif CC.DrivingStage %3 == 3:   # prepares for next set of tiles
            print(3)
            Move_Arm("open")
            End_of_stage = True
    else:
        END("Task completed! - End")
        break
    

    # managing the game log
    print(log)
    log = ""