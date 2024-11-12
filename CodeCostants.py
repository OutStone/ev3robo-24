DriveSpeed = 800 # in mm/s
DrivingStage = 1 # changes with every turn

DistanceSensor_Offset = 10 # in cm from the ball eating part

Do_ColorSort = True 
StageValues = {
    1 : 70 - DistanceSensor_Offset, # Wall distance in cm 
    2 : None,
    3 : None,
    4 : 280, # Drive distance in mm
    5 : 42 - DistanceSensor_Offset, # Wall distance in cm
    6 : None,
    7 : None 
    # for eight I will need a drive distance again    
}

##--##--## Constants for sorting 
SortingSpeed = 100 # in deg/s
SortAngle = {
    'red' : 0, # TODO: find the correct value
    'blue' : 0 # TODO: find the correct value
}

##--##--## Constants for following wall with a sensor ##--##--##
WallDistance = 30 # in % from the sensors maximum
        # TODO: the distances will differ in value based on the drive line we are in
linKoef = 0.05
expKoef = 3

DistanceAvrg = []
Values_in_Avrg = 5 # 10 for infraRed
MaxCorrection = 70

##--##--## Constants for turning function  ##--##--##
TurnErr = 1/6.5 # TODO: set a error value before each run