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

robot = DriveBase() # TODO: set this up!
LeftMotor = Motor() # TODO: set this up!
RightMotor = Motor() # TODO: set this up!

##--##--##--## CODE CONSTANTS ##--##--##--##
import CodeCostants as CC

##--##--##--## Mechanical wall follow ##--##--##--##
UNI_SearchingForWall = True
UNI_MechSpeed = CC.DriveSpeed

# set up function resets all variables for Follow_Mech()
def Follow_Mech_SetUp(Side = "right",Reverse=False,Speed=1):
    global UNI_SearchingForWall,UNI_MechSpeed

    UNI_MechSpeed *= Speed
    UNI_SearchingForWall = True

    if lower(Side) == 'left':
        CC.FollowAngle['ok'] *= -1
        CC.FollowAngle['btn-off'] *= -1
    
    if Reverse:
        UNI_MechSpeed *= -1
    

# the function itself
def Follow_Mech():
    global UNI_SearchingForWall

    if SideBtn.pressed(): # if True then we are directly next to wall
        robot.drive(UNI_MechSpeed, CC.FollowAngle['ok'])
        UNI_SearchingForWall = False

    else: # we aren't next to wall -> turn to side and search for it 
        if not UNI_SearchingForWall:
            Drive_Clock.reset()
            Drive_Clock.resume()
            UNI_SearchingForWall = True
            robot.drive(UNI_MechSpeed, CC.FollowAngle['btn-off'])

        elif Drive_Clock.time() > 1000:
            robot.drive(UNI_MechSpeed, 0)


##--##--##--## wall follow with ultrasonic sensor ##--##--##--##
UNI_previous_error = 0
UNI_integral = 0

# set up function resets all variables for Follow_Ultra()
def Follow_Mech_SetUp():
    global UNI_integral,UNI_previous_error
    UNI_integral = 0
    UNI_previous_error = 0

# the function itself
def Follow_Ultra(target):
        global integral, UNI_previous_error
        dist = UlraSensor.distance()/10

        error = target - dist

        UNI_integral += error
        derivative = error - UNI_previous_error

        correction = CC.proportial_gain * error + CC.integral_gain * UNI_integral + CC.derivative_gain * derivative
        UNI_previous_error = error

        left_speed = CC.DriveSpeed + correction
        right_speed = CC.DriveSpeed - correction

        RightMotor.run(left_speed)
        LeftMotor.run(right_speed)

##--##--##--## function for turning ##--##--##--##
def ServoTurn(left, right, speed): # ratio between the wheels, last param is speed in deg/s
    robot.stop()

    Angle_left = (RC.Axle_Track/(4*RC.Wheel_Diameter)) * left * 180*-1
    Angle_right = (RC.Axle_Track/(4*RC.Wheel_Diameter)) * right * 180

    Speed_left = speed * left
    Speed_right = speed * right

    RightMotor.run_angle( Speed_right, Angle_right,wait=False )
    LeftMotor.run_angle( Speed_left, Angle_left )
    print("konec zataceni")

    robot.stop()