DriveSpeed = 800 # in mm/s
GameStage = 1 # after dumping the red & blue balls this will change to 2
SortingSpeed = 100 # in deg/s
SortAngle = {
    'red' : 0, # TODO: find the correct value
    'blue' : 0 # TODO: find the correct value
}

WallDistance = 30 # in % from the sensors maximum
        # TODO: the distances will differ in value based on the drive line we are in
linKoef = 0.02
expKoef = 3

DistanceAvrg = []
Values_in_Avrg = 7 # 10 for infraRed