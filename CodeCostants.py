DriveSpeed = 300 # in mm/s
DrivingStage = 1 # changes with every turn
GamePart = 1
RunSecondPart = True

UltraSensorMax = 255
DistanceSensor_Offset = 10 # in cm from the ball eating part

EndRun = -1 # TESTING ONLY

Do_ColorSort = True 
StageValues = {
    1 : 717,    # distance from wall where should stop
    2: "close", 
    3: 717,     # distance to drive back to reach wall (TODO: correct it by including dimensions of robot)
}
UltraFollowStages = []
ReverseTurns = []
DoNotTurn = []

##--##--## Constants for gate operating 
GateSpeed = 500 # in deg/s
GateAngle = 360

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
##--##--## Constants for turning function  ##--##--##
TurnErr = 10/9 #CHECK: check at the competition