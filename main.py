#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

##--##--##--## ROBO CONSTANTS ##--##--## 
from RoboConstants.py import ( Motors, Buttons, ColorSensor_port,
                                Wheel_Diameter, Axle_Track )
# TODO: test if I can just import the file without specifing the variables to be imported
RUN = True

##--##--##--## CODE CONSTANTS ##--##--##--##
import CodeConstants

##--##--##--## ROBO SET UP ##--##--## 
Ev3 = EV3Brick()

# Motors
LeftMotor = Motor( Motors['left'],positive_direction = Direction.COUNTERCLOCKWISE )
RightMotor = Motor( Motors['right'],positive_direction = Direction.COUNTERCLOCKWISE )

SortingMotor = Motor( Motors['sort'],positive_direction = Direction.COUNTERCLOCKWISE )

robot = DriveBase( LeftMotor, RightMotor, Wheel_Diameter, Axle_Track )

# Sensors
ColorSensor = ColorSensor( ColorSensor_port )

FrontBtn =  TouchSensor( Buttons['front'] )

print( ColorSensor.rgb() )

##--##--##--## CHECKING THE COLORS ##--##--## 

# sorts the ping pong balls based on highest rgb value - red or blue
def color( inputColor, stage ):
    Sorting = True
    red = inputColor[0]
    green = inputColor[1]
    blue  = inputColor[2]

    match stage:
        case 1:
            if red > blue:
                print('red')
                SortingMotor.run_angle(SortingSpeed, SortAngle['red'], then=Stop.HOLD, wait=False)

            elif blue > red:
                print('blue')
                SortingMotor.run_angle(SortingSpeed, SortAngle['blue'], then=Stop.HOLD, wait=False)

        case 2:
            # no need to sort by color - balls are just picked up to be throwed on oponent's side  
            SortingMotor.run_angle(SortingSpeed, SortAngle['red'], then=Stop.HOLD, wait=False)


##--##--##--## GAME LOOP ##--##--##--##

turn_count = 0
Sorting = False

while RUN:
    robot.drive(DriveSpeed,0)

    # color detection
    isColor = ColorSensor.color()
    if isColor != None and not Sorting:
        detectedColor = ColorSensor.rgb()
        color( colorDetected, GameStage )

    elif isColor == None:
        Sorting = False
        # TODO: some kind of control if the sorting mechanism is on home positions

    # collision detection
    if FrontBtn.pressed():
        robot.stop()
        robot.turn(90)
        turn_count += 1

        # break the program
        if turn_count == 5:
            break
        # TODO: get this system to drive throught the game map as planneds