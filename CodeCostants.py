import RoboConstants as RC

DriveSpeed = 800 # in mm/s
RotationSpeed = 360 * DriveSpeed/(RC.Wheel_Diameter*3.14) # in deg/s
DrivingStage = 1 # changes with every turn

UltraSensorMax = 2550
DistanceSensor_Offset = {
    "backwards" : 160,
    "sideways" : 50
} # in cm from the ball eating part

EndRun_at = 20 # TESTING ONLY

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
    10: 1280,
    11: 1010,
    
    12: 840,  # in deg - dist for arm to drive
    13: 1200,
    14: 1010,
    
    15: 1230,  # in deg - dist for arm to drive
    16: 1120,
    17: 1010,
    
    18: -100, # in deg - dist for arm to drive
    19: "open",
    20: "close",

    # squares
    21: 360,   # in deg - dist for arm to drive
    22: 1500,  # TODO: try this
    23: 1350,  # TODO: try this

    21: 840,   # in deg - dist for arm to drive
    22: 1500,  # TODO: try this
    23: 1350,  # TODO: try this
    
    18: -100, # in deg - dist for arm to drive
    19: "open",
    20: "close",
}

##--##--## Constants for gate operating ##--##--##
ArmSpeed = 800 *0.75 # in deg/s #TODO: reducing koef
ArmDist = 900 # in mm
way_in_degs = 360*900/(RC.ArmWheelDiameter*6.3)

##--##--## Time Constants (in ms) ##--##--##
LoopTime = 20
GameLenght = 90 * 1000