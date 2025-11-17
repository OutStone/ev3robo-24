import RoboConstants as RC

DriveSpeed = 400 # in mm/s
RotationSpeed = 360 * DriveSpeed/(RC.Wheel_Diameter*3.14) # in deg/s
DrivingStage = 2 # changes with every turn

UltraSensorMax = 2550
DistanceSensor_Offset = {
    "backwards" : 200,
    "sideways" : 50
} # in cm from the ball eating part

EndRun_at = -1 # TESTING ONLY

StageValues = {
    2: "open",
    3: "close",
    4: 570, # in mm
    5: "open",
    6: "close",
    7: 840, # in mm
    8: "open",
    9: "close",
    4: 1110 # in mm
}

##--##--## Constants for gate operating ##--##--##
ArmSpeed = 800 # in deg/s
ArmDist = 900 # in mm

##--##--## Time Constants (in ms) ##--##--##
LoopTime = 20
GameLenght = 90 * 1000