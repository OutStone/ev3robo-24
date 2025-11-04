import RoboConstants as RC

DriveSpeed = 400 # in mm/s
RotationSpeed = 360 * 400/(RC.Wheel_Diameter*3.14) # in deg/s
DrivingStage = 0 # changes with every turn
GamePart = 1
RunSecondPart = True

UltraSensorMax = 2550
DistanceSensor_Offset = {
    "backwards" : 250,
    "sideways" : 50
} # in cm from the ball eating part

EndRun = -1 # TESTING ONLY

Do_ColorSort = True 
StageValues = {
    0: "open",
    1: 1100,#700,    # distance from wall where should stop
    2: "close", 
    3: -710,    # distance to drive back to reach wall
    4: 0.25     # fraction of circle to steer
}
MotorsRunSeparately = [1]

##--##--## Constants for gate operating ##--##--##
GateSpeed = 200 # in deg/s
GateAngle = 90

##--##--## Time Constants (in ms) ##--##--##
LoopTime = 20
GameLenght = 90 * 1000

##--##--## Constants for following wall with a sensor ##--##--##
proportial_gain = 5
derivative_gain = 50

##--##--## Constants for mechanical following ##--##--##
FollowAngle = {
    'ok' : 3,
    'btn-off' : -25
}

##--##--## Constants for line following ##--##--##
white_koef = 0.4
black_koef = 0.4

##--##--## Constants for turning function  ##--##--##
TurnErr = 10/9 #CHECK: check at the competition