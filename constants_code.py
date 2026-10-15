Speeds = {
    'main': 90,
    'arm' : 360
}


EndRun_at = -1 # TESTING ONLY

Deg_vals = [
    0,
    100,
    250,
    450,
    600,
    750,
    900,
   1050
]

Arm_start = 5.5 *1000

Arm_in = [
    0.5   * 1000,
    1     * 1000,
    0.5   * 1000,
    0     * 1000,
    0,
    0.5   * 1000,
    1     * 1000,
    0
]

Arm_out = [
    5.5 * 1000,
    5.5 * 1000,
    3.8 * 1000,
    4   * 1000,
    5   * 1000,
    4   * 1000,
    4   * 1000,
    Arm_in[-1] #tj. nestane se zadny pohyb
]



Turn_piece = [
    100, # arm rotation in degs
    0,
    200,
    0,
    0,
    1,
    0,
    1
]

##--##--## Time Constants (in ms) ##--##--##
GameLenght = 90 * 1000