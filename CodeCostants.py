import RoboConstants as RC

DriveSpeed = 400 # in mm/s
RotationSpeed = 360 * DriveSpeed/(RC.Wheel_Diameter*3.14) # in deg/s
DrivingStage = 1 # changes with every turn

UltraSensorMax = 2550
DistanceSensor_Offset = {
    "backwards" : 200,
    "sideways" : 50
} # in cm from the ball eating part

EndRun_at = -1 # TESTING ONLY

StageValues = {
    1: "close",
    2: "open",
    3: 840, # in mm
    4: "close",
    5: 400, # in mm
    6: "open", 
    7: 570, # in mm
    8: "close",
    9: "open"
}

##--##--## Constants for gate operating ##--##--##
ArmSpeed = 800 # in deg/s
ArmDist = 900 # in mm

##--##--## Time Constants (in ms) ##--##--##
LoopTime = 20
GameLenght = 90 * 1000