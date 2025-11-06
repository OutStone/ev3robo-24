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
    
    # wait for the robot to start moving
    print('Angle_left:',Angle_left)
    wait(90)
    Angle_before = Angle_start
    Angle_now = LeftMotor.angle()

    # while there is a detected movement of robot, it will repeatedly search for black color
    while round(Angle_now,1) != round(Angle_before,1):
        detectedColor = ColorSensor.color()
        print("     detected color:",detectedColor)
        
        # found our target so stop any other movement
        if detectedColor == Color.BLACK:
            robot.stop
            print("-/-/-/-/- task completed -/-/-/-/-",LeftMotor.angle())
            break
        
        # wait for robot to move a bit -> update robots position
        wait(15)
        Angle_before = Angle_now
        Angle_now = LeftMotor.angle()
        print("now at:",Angle_now)
    
    # respond with the result
    robot.stop()
    return ColorSensor.color() == Color.BLACK
    
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
    