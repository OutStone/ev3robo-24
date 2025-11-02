#!/usr/bin/env pybricks-micropython
from pybricks.parameters import Port

Motors = {
    'left'  : Port.C,
    'right' : Port.B,
    'third' : Port.D
}
Buttons = {
    'front' : Port.S1,
    'side'  : Port.S2
}

ColorSensor_port = Port.S3
Gyro_port = Port.S3 # Not on robot

InfraSensor_port = Port.S4 # Not on robot
UlraSensor_port = Port.S4

Wheel_Diameter = 55 # in milimeters
Axle_Track = 130 # in mm - small testing robo had just 76 mm