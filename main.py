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
    DriveMotor = Motor( RC.Motors['drive'],positive_direction = Direction.CLOCKWISE )
    ArmMotor = Motor( RC.Motors['arm'],positive_direction = Direction.COUNTERCLOCKWISE )
    #ThirdMotor = Motor( RC.Motors['third'],positive_direction = Direction.CLOCKWISE )


    # Sensors
    Btn_1 = TouchSensor( RC.Buttons['1'] )
    Btn_2 = TouchSensor( RC.Buttons['2'] )

    # ColorSensor = ColorSensor( RC.ColorSensor_port )

    # Gyro = GyroSensor( RC.Gyro_port )
    # InfraSensor = InfraredSensor( RC.InfraSensor_port )
    UlraSensor = UltrasonicSensor( RC.UlraSensor_port )

##--##--##--## Driving Funcions ##--##--##--##
def Stop_Dist(target,direction="forward"):
    global log

    dist = UlraSensor.distance() + CC.DistanceSensor_Offset['backwards']
    log += str(dist) + "     "
    if dist >= CC.UltraSensorMax:
            print("\033[92m Ultra reporting max value \033[00m")
            return True
    
    #robo is going forward => wants a bit higher dist than target
    elif direction.lower() == "forward" and dist >= target: 
            return True
    
    #robo is going backward => wants a bit higher dist than target
    if direction.lower() == "backward" and dist <= target: 
            return True
    
    return False

##--##--##--## working with tetris tiles ##--##--## 
def Move_Arm(direct):
    # this func does back and forth movement with robot's arm
    if direct.lower() == "open":
        flag = 1.2
    elif direct.lower() == "close":
        flag = -1.2 #TODO: trim
    else:
        print("\033[91m incorrect direction input to gate moving func '{}'\033[00m ".format(direct))

    ArmMotor.run_target(
        CC.ArmSpeed,
        12000*flag 
    )

def Stop_Arm_at(place):
    ArmMotor.run_target(
        CC.ArmSpeed
    )

    GO = True
    while GO:  
        wait(10)
        if place == 1:
            GO = Btn_1.pressed()
        elif place == 2:
            GO = Btn_2.pressed()
        elif place == 3:
            pass
            # if needed, than here will be sth. with color sensor

    ArmMotor.stop()
            
def Stepper_Arm(dist):
    ArmMotor.run_angle(
        CC.ArmSpeed,
        360*dist/(6.3*RC.ArmWheelDiameter)
    )
    ArmMotor.stop()
            
       
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
    if Btn_1.pressed():
        Start = True
    elif Start:
        # upon releasing the button (may take multiple game cycles) starts the game
        Game_Clock.resume()
        Cycle_Clock.resume()
        break


while True: # game loop
    
    if Game_Clock.time() >= CC.GameLenght:
        # the game time is up => robot should stop
        END("Time is up! - End")
        break

    # next stage triggered -> reseting before next game stage 
    if End_of_stage:
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
        print("\033[97m     from start   : \033[93m",Game_Clock.time()/1000,
              "\033[97m     left         : \033[93m"  +    str((   Game_Clock.time() - CC.GameLenght )/1000),
              "\033[97m     stage lenght : \033[93m:",(  Game_Clock.time() - StageStartTime )/1000)
        print('\033[00m',CC.DrivingStage)
        StageStartTime = Game_Clock.time()

        # forced stop
        if CC.DrivingStage == CC.EndRun_at:
            END("Forced End")
            break


    # driving stage logic
    if   CC.DrivingStage == 1:   # stacks tiles in front of storage
            Move_Arm("close")
            End_of_stage = True
    elif CC.DrivingStage == 2:   # prepares for next set of tiles
            Move_Arm("open")
            End_of_stage = True
    elif CC.DrivingStage == 3:   # drives to next set of bricks
            DriveMotor.run(CC.RotationSpeed)
             # if I reached the target it returns True => next stage will activite
            End_of_stage = Stop_Dist(CC.StageValues[ CC.DrivingStage ] - CC.DistanceSensor_Offset["backwards"])
            
    elif CC.DrivingStage == 4:   # stacks tiles in storage
            Move_Arm("close")
            End_of_stage = True
    elif CC.DrivingStage == 5:   # drives back to next set of bricks - storage is kept closed with arm
            DriveMotor.run(CC.RotationSpeed)
            End_of_stage = Stop_Dist(
                 CC.StageValues[ CC.DrivingStage ] - CC.DistanceSensor_Offset["backwards"],
                 "backwards")
            
    elif CC.DrivingStage == 6:  # prepares for next set of tiles
            Move_Arm("open")
            End_of_stage = True
    elif CC.DrivingStage == 7:  # drives to next set of bricks
            DriveMotor.run(CC.RotationSpeed)
            End_of_stage = Stop_Dist(CC.StageValues[ CC.DrivingStage ] - CC.DistanceSensor_Offset["backwards"])

    elif CC.DrivingStage == 8:   # stacks tiles in front of storage
            Move_Arm("close")
            End_of_stage = True
    elif CC.DrivingStage == 9:   # prepares for next set of tiles
            Move_Arm("open")
            End_of_stage = True 
    else:
        END("Task completed! - End")
        break
    

    # managing the game log
    print(log)
    log = ""