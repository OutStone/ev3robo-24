#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase

##--##--##--## ROBO CONSTANTS ##--##--## 
import RoboConstants as RC

##--##--##--## CODE CONSTANTS ##--##--##--##
import CodeCostants as CC

##--##--##--## ROBO SET UP ##--##--##
if True:
    # Motors
    LeftMotor = Motor( RC.Motors['left'],positive_direction = Direction.CLOCKWISE )
    RightMotor = Motor( RC.Motors['right'],positive_direction = Direction.CLOCKWISE )
    
    robot = DriveBase( LeftMotor, RightMotor, RC.Wheel_Diameter, RC.Axle_Track )
    robot.settings(straight_speed=2*CC.DriveSpeed)

    # Sensors
    ColorSensor = ColorSensor( RC.ColorSensor_port )

##--##--##--## Driving Funcions ##--##--##--##
def Look_for_Line(search_angle,speed):
    # safe the beginning position
    Angle_start = LeftMotor.angle()
    
    # calculating the turn
    Angle_left  = (RC.Axle_Track/RC.Wheel_Diameter) * search_angle * -1 * 360
    Angle_right = (RC.Axle_Track/RC.Wheel_Diameter) * search_angle      * 360

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

        # found our target so stop any other movement
        if detectedColor == Color.BLACK:
            robot.stop
            Succes = True
            print("-/-/-/-/- task completed -/-/-/-/-",LeftMotor.angle())
            break

        # update our turn-describing variables
        Angle_driven = LeftMotor.angle() - Angle_start
        print("now at:",Angle_driven)
    
    # robot had come over black color
    if Succes:
        wait(50)
        print("                 data:",ColorSensor.color())
        # if robot found the correct color it had oversteared (always happens)
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
    
##--##--##--## Logic of algorithm ##--##--##--##
#  Turn to angle alpha asynchronously
#     - meanwhile read the color sensor 
#     - stop motors when
#               - black color detected  ==> objective accomplished
#               - turning completed whithout color detection  ==> check the other side
#
# OTHER SIDE
#  Turn to angle -2*alpha asynchronously
#     - meanwhile read the color sensor 
#     - stop motors when
#               - black color detected 
#               - turning completed whithout color detection  ==> throw error

##--##--##--## GAME LOOP ##--##--##--##
aplha = 1/6
Found = Look_for_Line(aplha,CC.RotationSpeed/4)
if not Found:
    Found = Look_for_Line(-2*aplha,CC.RotationSpeed/4)

if Found:
    print("done!")
elif not Found:
    print("the line is nowhere to be found :(")
    