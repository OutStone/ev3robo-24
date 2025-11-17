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
    ThirdMotor = Motor( RC.Motors['third'],positive_direction = Direction.COUNTERCLOCKWISE )
    LeftMotor = Motor( RC.Motors['left'],positive_direction = Direction.CLOCKWISE )
    RightMotor = Motor( RC.Motors['right'],positive_direction = Direction.CLOCKWISE )

    robot = DriveBase( LeftMotor, RightMotor, RC.Wheel_Diameter, RC.Axle_Track )
    robot.settings(straight_speed=2*CC.DriveSpeed)

    # Sensors
    FrontBtn = TouchSensor( RC.Buttons['front'] )
    SideBtn = TouchSensor( RC.Buttons['side'] )

    ColorSensor = ColorSensor( RC.ColorSensor_port )

    # Gyro = GyroSensor( RC.Gyro_port )
    # InfraSensor = InfraredSensor( RC.InfraSensor_port )
    UlraSensor = UltrasonicSensor( RC.UlraSensor_port )

##--##--##--## Driving Funcions ##--##--##--##
def ServoTurn(fraction_of_circle, speed): # in deg/s & deg
    robot.stop() # TODO: potentionaly too redundant -> remove after a check of functions usage in code

    Angle_left  = (RC.Axle_Track/RC.Wheel_Diameter) * fraction_of_circle * -1 * 360
    Angle_right = (RC.Axle_Track/RC.Wheel_Diameter) * fraction_of_circle      * 360

    RightMotor.run_angle( speed, Angle_right,wait=False )
    LeftMotor.run_angle(  speed, Angle_left )
    print("konec zataceni")

    robot.stop()

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

def Follow_Ultra(target):
        global previous_error
        dist = UlraSensor.distance()

        error = target - dist

        derivative = error - previous_error

        correction = CC.proportial_gain * error + CC.derivative_gain * derivative
        previous_error = error

        left_speed = CC.RotationSpeed + correction
        right_speed = CC.RotationSpeed - correction

        RightMotor.run(left_speed)
        LeftMotor.run(right_speed)

def Follow_Mechanical():
    global Lost_the_wall
    if SideBtn.pressed(): # True -> we are directly next to wall
        robot.drive(CC.DriveSpeed, CC.FollowAngle['ok'])
        Lost_the_wall = False
    else: # time to search where the lost wall is
        if not Lost_the_wall:
            Drive_Clock.reset()
            Drive_Clock.resume()
            Lost_the_wall = True
            robot.drive(CC.DriveSpeed, CC.FollowAngle['btn-off'])
        elif Drive_Clock.time() > 1000:
            robot.drive(CC.DriveSpeed * 3.14 * RC.Wheel_Diameter/360, 0)

def Follow_Color():
    global log
    Color_now = ColorSensor.color()
    log += str(Color_now) + "     "
    if Color_now == Color.BLACK: # now it wants to find white => turning left
        RightMotor.run(CC.RotationSpeed*(1-CC.black_koef))
        LeftMotor.run(CC.RotationSpeed *(1+CC.black_koef))
        
    elif Color_now == Color.WHITE: # now it wants to find black => turning right
        RightMotor.run(CC.RotationSpeed*(1+CC.white_koef))
        LeftMotor.run(CC.RotationSpeed *(1-CC.white_koef))

    else: # this is the same as for white, but it should not happen so better make a note in game log
        log += "\033[93m LACK OF LIGHT:\033[00m " # in Yellow
        RightMotor.run(CC.RotationSpeed*(1+CC.white_koef))
        LeftMotor.run(CC.RotationSpeed *(1-CC.white_koef))
    log += str(Color_now) + "     "

def Look_for_Line(circle_fraction,speed):
    # safe the beginning position
    Angle_start = LeftMotor.angle()
    
    # calculating the turn
    Angle_left  = (RC.Axle_Track/RC.Wheel_Diameter) * circle_fraction * -1 * 360
    Angle_right = (RC.Axle_Track/RC.Wheel_Diameter) * circle_fraction      * 360

    RightMotor.run_angle( speed, Angle_right,wait=False)
    LeftMotor.run_angle(  speed, Angle_left, wait=False)

    # variables describing if the turn is over
    Angle_driven = LeftMotor.angle() - Angle_start
    Angle_target = Angle_left
    print('Angle_target:',Angle_target)
    Succes = False

    # loop to read colors around robot while its turning - loop stops when we reach 95% of the target angle to search through
    while abs(Angle_target*0.95) > abs(Angle_driven): 
        detectedColor = ColorSensor.color()
        print("     detected color:",detectedColor)

        # found our target so stop any movement
        if detectedColor == Color.BLACK:
            robot.stop
            Succes = True
            print("-/-/-/-/- succesfully found the line -/-/-/-/-",LeftMotor.angle())
            break

        # update our turn-describing variables
        Angle_driven = LeftMotor.angle() - Angle_start
        print("now at:",Angle_driven)
    
    # robot had come over black color
    if Succes:
        wait(50)
        print("                 data:",ColorSensor.color())
        # if robot found the correct color it had oversteared (isn't preventable in higher speeds)
        #   => now it will slowly go back - first milestone is finding black, and second one is finding its right edge (from robo prespective) 
        if Angle_left < 0:
            going_from_left = True
            Flip = 1
        else:
            going_from_left = False
            Flip = 0
        
        # constantly turning
        RightMotor.run( 0.1*speed * (-Flip))
        LeftMotor.run(  0.1*speed *   Flip)

        # wasting time 'till robot reaches black color
        i = 0
        
        detectedColor = ColorSensor.color()
        while detectedColor != Color.BLACK:
            wait(5)
            print(i)
            i+=1
            detectedColor = ColorSensor.color()
        else:
            robot.stop()
        
        if going_from_left: # we want to reach the other side of the black line -> stop when everything else than black
            print("inside")
            RightMotor.run( 0.2*speed * (-Flip))
            LeftMotor.run(  0.2*speed *   Flip )

            detectedColor = ColorSensor.color()
            while detectedColor == Color.BLACK:
                wait(5)
                i+=1
                detectedColor = ColorSensor.color()
                print(i,detectedColor)
            else:
                robot.stop()
        return True
    else: # it hadn´t found black color  
        return False
##--##--##--## working with tetris tiles ##--##--## 
def Move_Gate(direct,wait_for_it=True):
    # this func does both open & close the gate
    if direct.lower() == "open":
        flag = 1
    elif direct.lower() == "close":
        flag = -1
    else:
        print("\033[91m incorrect direction input to gate moving func '{}'\033[00m ".format(direct))

    ThirdMotor.run_angle(
        CC.GateSpeed,
        CC.GateAngle * flag,
        then=Stop.HOLD,
        wait=wait_for_it
    )
    
##--##--##--## GAME LOOP ##--##--##--##
if True: # set up of variables
    # driving
    End_of_stage = False # substitutes for a button press -> iniciates a robot turn
    Lost_the_wall = False # zero.. everything ok;  1 ... a problem -> trying to drive back to target

    # ultrasonic wall follow
    previous_error = 0

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
    if SideBtn.pressed():
        Start = True
    elif Start:
        # upon releasing the button (may take multiple game cycles) starts the game
        Game_Clock.resume()
        Cycle_Clock.resume()
        break

while True: # game loop
    
    if Game_Clock.time() >= CC.GameLenght:
        # the game time is up => robot should stop
        robot.stop()
        Ev3.speaker.beep()
        print("\033[92m Time is up! - End\033[00m")
        break

    # next stage triggered -> reseting before next game stage 
    if FrontBtn.pressed() or End_of_stage:
        # reseting driving clock
        Drive_Clock.pause()
        Drive_Clock.reset()

        # reseting variables
        CC.DrivingStage += 1
        End_of_stage = False
        previous_error = 0
        Lost_the_wall = False

        # stoping the robot after movent
        robot.stop()

        # time logging
        print("         time:",Game_Clock.time()/1000,
              "  T"  +    str((   Game_Clock.time() - CC.GameLenght )/1000),
              "stage lenght:",(  Game_Clock.time() - StageStartTime )/1000)
        StageStartTime = Game_Clock.time()

        # forced stop
        if CC.DrivingStage == CC.EndRun:
            Ev3.speaker.beep()
            print("\033[92m Forced End\033[00m")
            break


    # driving stage logic
    if  CC.DrivingStage == 0:   # opens the storage
        End_of_stage = True
        Move_Gate(CC.StageValues[ CC.DrivingStage ])
    elif CC.DrivingStage == 1:  # color follow  && max distance from wall to reach
        Follow_Color()
        End_of_stage = Stop_Dist(CC.StageValues[ CC.DrivingStage ] - CC.DistanceSensor_Offset["backwards"]) # if I reached the target it returns True => next stage will activite
    elif CC.DrivingStage == 2:  # closes the storage
        End_of_stage = True
        Move_Gate(CC.StageValues[ CC.DrivingStage ])
    elif CC.DrivingStage == 3:  # reverse to the other side of game plan
        robot.straight(CC.StageValues[ CC.DrivingStage ] + CC.DistanceSensor_Offset[ 'backwards' ])
        End_of_stage = True
    elif CC.DrivingStage == 4:  # a right angle turn
        ServoTurn(-0.25 , CC.RotationSpeed)
        End_of_stage = True

    elif CC.DrivingStage == 5:
        # in future: Move_Gate
        End_of_stage = True
    elif CC.DrivingStage == 6:
        # in future: Follow_Ultra

        # constant time program cycle
        if Cycle_Clock.time() < CC.LoopTime: # spare time -> waits
            wait(CC.LoopTime - Cycle_Clock.time())

        else: # not enought time
            pass
            print('\033Err: cycle took to long!\033',Cycle_Clock.time()) # printing in red color
    
        Cycle_Clock.reset()

        End_of_stage = True
    elif CC.DrivingStage == 7:
        # in future: reverse to let tetris tiles lie on the corect place
        End_of_stage = True
    elif CC.DrivingStage == 8:
        # in future: ServoTurn(0.5 , CC.RotationSpeed)
        End_of_stage = True

    elif CC.DrivingStage == 9:  # mech wall follow  && max distance from wall to reach
        # Follow_Mechanical()
        LeftMotor.run(CC.RotationSpeed)
        RightMotor.run(CC.RotationSpeed)
        End_of_stage = Stop_Dist(CC.StageValues[ CC.DrivingStage ])
    elif CC.DrivingStage == 10: # a right angle turn
        ServoTurn(-0.4 , CC.RotationSpeed)
        wait(1000)
        End_of_stage = True
    elif CC.DrivingStage == 11: # searching for colored line
        Found = Look_for_Line(CC.SearchAngle,CC.RotationSpeed/4)
        if not Found:
            Found = Look_for_Line(-2*CC.SearchAngle,CC.RotationSpeed/4)
        print("Found:",Found)
        End_of_stage = Found
    elif CC.DrivingStage == 12:
        Follow_Color()
        End_of_stage = Stop_Dist(CC.StageValues[ CC.DrivingStage ] - CC.DistanceSensor_Offset["backwards"])
    else:
        Ev3.speaker.beep()
        print("\033[92m End\033[00m")
        break
    

    # managing the game log
    print(log)
    log = ""