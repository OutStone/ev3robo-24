import RoboConstants as RC

DriveSpeed = 800 # in mm/s
RotationSpeed = 360 * DriveSpeed/(RC.Wheel_Diameter*3.14) # in deg/s
DrivingStage = 22 # changes with every turn

UltraSensorMax = 2550
DistanceSensor_Offset = {
    "backwards" : 160,
    "sideways" : 50
} # in cm from the ball eating part

EndRun_at = -1 # TESTING ONLY

StageValues = {
    1 : "open",
    2 : "close",
    3 : 590, # in mm
    4 : "open",
    5 : "close",
    6 : 1010, # in mm
    7 : "open",
    8 : "close",

    # big I's
    9 : 360,  # in deg - dist for arm to drive
    10: 900,
    11: 0,
    
    12: 900,  # in deg - dist for arm to drive
    13: 650,
    14: 0,
    
    15: 1500,  # in deg - dist for arm to drive
    16: 450,
    17: 0,
    
    18: -100, # in deg - dist for arm to drive
    19: 1150,
    20: "open",
    21: "close",

    # squares
    22: 360,   # in deg - dist for arm to drive
    23: 700,  # TODO: try this
    24: 0,  # TODO: try this

    25: 900,   # in deg - dist for arm to drive
    26: 700,  # TODO: try this
    27: 0,  # TODO: try this
    
    28: -100, # in deg - dist for arm to drive
    29: 1100,
    30: "open",
    31: "close",
    31: 2000
}

##--##--## Constants for gate operating ##--##--##
ArmSpeed = 800 *0.75 # in deg/s #TODO: reducing koef
ArmDist = 900 # in mm
way_in_degs = 360*900/(RC.ArmWheelDiameter*6.3)

##--##--## Time Constants (in ms) ##--##--##
LoopTime = 20
GameLenght = 90 * 1000