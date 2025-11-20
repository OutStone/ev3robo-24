#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

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
    # Btn_2 = TouchSensor( RC.Buttons['2'] )

    # ColorSensor = ColorSensor( RC.ColorSensor_port )

    # Gyro = GyroSensor( RC.Gyro_port )
    # InfraSensor = InfraredSensor( RC.InfraSensor_port )
    UlraSensor = UltrasonicSensor( RC.UlraSensor_port )

##--##--##--## Driving Funcions ##--##--##--##
def Stop_Dist(target,direction="forward"):
    global Buffer

    dist = UlraSensor.distance() + CC.DistanceSensor_Offset['backwards']
    print(dist)
    if dist >= CC.UltraSensorMax:
            print("\033[92m Ultra reporting max value \033[00m")
            if Buffer:
                 return True
            Buffer = True
    
    #robo is going forward => wants a bit higher dist than target
    elif direction.lower() == "forward" and dist >= target: 
            return True
    
    #robo is going backward => wants a bit higher dist than target
    if direction.lower() == "backward" and dist <= target:
            print("yes:",dist,target,dist <= target)
            return True
    else:
            Buffer = False
    
    return False

def Stepper_Drive(dist): # in deg
    DriveMotor.run_target(
        CC.ArmSpeed*0.5,
        dist
    )
    DriveMotor.stop()
   
##--##--##--## working with tetris tiles ##--##--## 
def Move_Arm(direct,K=1,asyncchornous=False):
    # this func does back and forth movement with robot's arm
    if direct.lower() == "open":
        degs = CC.way_in_degs*2.2
    elif direct.lower() == "close":
        degs = -180 #TODO: trim
    else:
        print("\033[91m incorrect direction input to gate moving func '{}'\033[00m ".format(direct))

    ArmMotor.run_target(
        CC.ArmSpeed*K,
        degs,
        wait= (not asyncchornous)
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
            # GO = Btn_2.pressed()
            pass
        elif place == 3:
            pass
            # if needed, than here will be sth. with color sensor

    ArmMotor.stop()
            
def Stepper_Arm(dist): # in deg
    ArmMotor.run_target(
        CC.ArmSpeed*0.5,
        dist
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

    Game_Clock = StopWatch() # for game timing
    Game_Clock.pause()
    Game_Clock.reset()
    StageStartTime = 0
        
    Cycle_Clock = StopWatch() # for stable game loops
    Cycle_Clock.pause()
    Cycle_Clock.reset()

Buffer = False
Start = False

Ev3.speaker.play_notes(['C4/4', 'C4/4', 'G4/4', 'G4/4'])
skip_btn = int(input("skip start btn? "))
while True and not skip_btn:
    if Btn_1.pressed():
        Start = True
    elif Start:
        # upon releasing the button (may take multiple game cycles) starts the game
        break

Game_Clock.resume()
Cycle_Clock.resume()

while True: # game loop
    
    if Game_Clock.time() >= CC.GameLenght:
        # the game time is up => robot should stop
        END("Time is up! - End")
        break

    # next stage triggered -> reseting before next game stage 
    if End_of_stage:

        # reseting variables
        CC.DrivingStage += 1
        End_of_stage = False
        Buffer = False

        # stoping the robot after movent
        DriveMotor.stop()
        ArmMotor.stop()

        # time logging
        print("\033[97m",CC.DrivingStage)
        print("\033[97m     from start   : \033[93m",Game_Clock.time()/1000,
              "\033[97m     left         : \033[93m"  +    str((   Game_Clock.time() - CC.GameLenght )/1000),
              "\033[97m     stage lenght : \033[93m:",(  Game_Clock.time() - StageStartTime )/1000)
        print('\033[00m',CC.DrivingStage)
        StageStartTime = Game_Clock.time()

        # forced stop - FOR DEBUG   
        if CC.DrivingStage == CC.EndRun_at:
            END("Forced End")
            break


    #--##--## driving stage logic
    # triangles
    if   CC.DrivingStage == 1:   # stacks tiles in front of storage
            Move_Arm("open",0.7)
            End_of_stage = True
    elif CC.DrivingStage == 2:   # prepares for next set of tiles
            Move_Arm("close")
            End_of_stage = True
    
    # bigs L's           
    elif CC.DrivingStage == 3:   # drives to next set of bricks
            DriveMotor.run(CC.RotationSpeed)
             # if I reached the target it returns True => next stage will activite
            End_of_stage = Stop_Dist(CC.StageValues[ CC.DrivingStage ] - CC.DistanceSensor_Offset["backwards"]) 
    elif CC.DrivingStage == 4:   # stacks tiles in front of storage
            Move_Arm("open")
            End_of_stage = True
    elif CC.DrivingStage == 5:   # prepares for next set of tiles
            Move_Arm("close")
            End_of_stage = True
    
    # bigs Z's           
    elif CC.DrivingStage == 6:   # drives to next set of bricks
            DriveMotor.run(CC.RotationSpeed)
            End_of_stage = Stop_Dist(CC.StageValues[ CC.DrivingStage ] - CC.DistanceSensor_Offset["backwards"]) 
    elif CC.DrivingStage == 7:   # stacks tiles in front of storage
            Move_Arm("open")
            End_of_stage = True
    elif CC.DrivingStage == 8:   # prepares for next set of tiles
            Move_Arm("close")
            End_of_stage = True
    
    # bigs I's   
    # 1
    elif CC.DrivingStage == 9:   # precisely moving the arm to position for repositioning of tile
            ArmMotor.reset_angle(0)
            Stepper_Arm(CC.StageValues[ CC.DrivingStage ])
            End_of_stage = True
    elif CC.DrivingStage == 10:   # pushes the tile forward
            DriveMotor.reset_angle(0)
            Stepper_Drive(CC.StageValues[ CC.DrivingStage ])
            End_of_stage = True
    elif CC.DrivingStage == 11:   # drives back to next set of bricks - storage is kept closed with arm
            Stepper_Drive(CC.StageValues[ CC.DrivingStage ])
            End_of_stage = True
    # 2    
    elif CC.DrivingStage == 12:   # precisely moving the arm to position for repositioning of tile
            Stepper_Arm(CC.StageValues[ CC.DrivingStage ])
            End_of_stage = True
    elif CC.DrivingStage == 13:   # pushes the tile forward
            Stepper_Drive(CC.StageValues[ CC.DrivingStage ])
            End_of_stage = True
    elif CC.DrivingStage == 14:   # drives back to next set of bricks - storage is kept closed with arm
            Stepper_Drive(CC.StageValues[ CC.DrivingStage ])
            End_of_stage = True
    # 3          
    elif CC.DrivingStage == 15:   # precisely moving the arm to position for repositioning of tile
            Stepper_Arm(CC.StageValues[ CC.DrivingStage ])
            End_of_stage = True
    elif CC.DrivingStage == 16:   # pushes the tile forward
            Stepper_Drive(CC.StageValues[ CC.DrivingStage ])
            End_of_stage = True
    elif CC.DrivingStage == 17:   # drives back to next set of bricks - storage is kept closed with arm
            Stepper_Drive(CC.StageValues[ CC.DrivingStage ])
            End_of_stage = True
    # stack them
    elif CC.DrivingStage == 18:   # precisely moving the arm to starting pos
            Stepper_Arm(CC.StageValues[ CC.DrivingStage ])
            End_of_stage = True
    elif CC.DrivingStage == 19:   # drives to next set of bricks
            Stepper_Drive(CC.StageValues[ CC.DrivingStage ])
            End_of_stage = True           
    elif CC.DrivingStage == 20:    # stacks tiles in front of storage
            Move_Arm("open")
            End_of_stage = True
    elif CC.DrivingStage == 21:   # prepares for next set of tiles
            Move_Arm("close")
            End_of_stage = True

    # squares   
    # 1
    elif CC.DrivingStage == 22:   # precisely moving the arm to position for repositioning of tile
            ArmMotor.reset_angle(0)
            Stepper_Arm(CC.StageValues[ CC.DrivingStage ])
            End_of_stage = True
    elif CC.DrivingStage == 23:   # pushes the tile forward
            Stepper_Drive(CC.StageValues[ CC.DrivingStage ])
            End_of_stage = True
    elif CC.DrivingStage == 24:   # drives back to next set of bricks - storage is kept closed with arm
            Stepper_Drive(CC.StageValues[ CC.DrivingStage ])
            End_of_stage = True
    # 2
    elif CC.DrivingStage == 25:   # precisely moving the arm to position for repositioning of tile
            Stepper_Arm(CC.StageValues[ CC.DrivingStage ])
            End_of_stage = True
    elif CC.DrivingStage == 26:   # pushes the tile forward
            Stepper_Drive(CC.StageValues[ CC.DrivingStage ])
            End_of_stage = True
    elif CC.DrivingStage == 27:   # drives back to next set of bricks - storage is kept closed with arm
            Stepper_Drive(CC.StageValues[ CC.DrivingStage ])
            End_of_stage = True
    # stack them
    elif CC.DrivingStage == 28:    # precisely moving the arm to position for repositioning of tile
            Stepper_Arm(CC.StageValues[ CC.DrivingStage ])
            End_of_stage = True
    elif CC.DrivingStage == 29:   # pushes the tile forward
            Stepper_Drive(CC.StageValues[ CC.DrivingStage ])
            End_of_stage = True          
    elif CC.DrivingStage == 30:    # stacks tiles in front of storage
            Move_Arm("open")
            End_of_stage = True        
    elif CC.DrivingStage == 31:    # stacks tiles in front of storage
            Move_Arm("close",1,True)
            End_of_stage = True

    # drive forward to be in the box
    elif CC.DrivingStage == 32:
            Stepper_Drive(CC.StageValues[ CC.DrivingStage ]) # drives forward hit the wall 
            End_of_stage = True 

    else:
        END("Task completed! - End")
        break

# Stepper_Drive(400) # in degs