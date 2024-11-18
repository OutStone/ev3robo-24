#!/usr/bin/env pybricks-micropython
from pybricks.parameters import Port

Motors = {
    'left'  : Port.A,
    'right' : Port.B,
    'sort'  : Port.C
}
Buttons = {
    'front' : Port.S4,
    'side'  : Port.S1
}

ColorSensor_port = Port.S3
Gyro_port = Port.S3 # Not on robot

InfraSensor_port = Port.S2 # Not on robot
UlraSensor_port = Port.S2

Wheel_Diameter = 55 # in milimeters
Axle_Track = 130 # in mm - small testing robo had just 76 mm