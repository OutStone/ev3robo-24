#!/usr/bin/env pybricks-micropython
from pybricks.parameters import Port

Motors = {
    'left' : Port.A,
    'right' : Port.D,
    'sort' : Port.B
}
Buttons = {
    'front' : Port.S4
}
ColorSensor_port = Port.S3
InfraSensor_port = Port.S2
UlraSensor_port = Port.S2

Wheel_Diameter = 55 # in milimeters
Axle_Track = 76 # in milemeters