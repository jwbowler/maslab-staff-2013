#Commander
LOG_FREQUENCY = .5 #seconds

BALL_BUTTON_TIMEOUT = 20

#Pins
IR_PINS = []
ULT_PINS =[(52,53),(50,51),(48,49),(46,47),(44,45),(42,43)]

COLOR_SWITCH_PIN = 11
RESET_BUTTON_PIN = 12

LEFT_MOTOR_PINS = (14,2,3)
RIGHT_MOTOR_PINS = (15,4,5)
ROLLER_HELIX_PINS = (13,6,7)
RAMP_SERVO_PIN = 9
SCORER_PIN = 16

#Data Collection
IR_POSITIONS = []

ULT_POSITIONS = [(.16,-108),(.16,-72),(.14,-36),(.09,0),(.14,36),(.16,72)]
ULT_TIMEOUT = 6000

#State Estimator
DIST_CAP = .8
ROBOT_RADIUS = .17
BALL_RADIUS = .02
BUTTON_CENTER_HEIGHT = .075
YELLOW_WALL_CENTER_HEIGHT = 0.06 # not counting blue stripe
TOWER_BASE_CENTER_HEIGHT = .075
TOWER_MIDDLE_CENTER_HEIGHT = .173
TOWER_MIDDLE_BOTTOM_HEIGHT = .146
TOWER_TOP_CENTER_HEIGHT = .27
TOWER_TOP_BOTTOM_HEIGHT = .243

#Goal Planning
ONLY_SCORE_PERIOD = 30

#Movement
HELIX_CYCLE_INTERVAL = 6

# Follow wall
WF_DIST_PID = (1.4, 0, .000, 0.35, 0) #1.5
WF_ANGLE_PID = (.028, 0, .0, 0.35, 0) #.05

WF_SLOWDOWN_DIST = .13
WF_STOP_DIST = .05

WF_ROT_LIM = .45
WF_DIST_TARGET = .30
WF_SPEED = .5
WF_MIN_WHEEL_SPEED = .2
WF_ROTATION = 1.0

WF_TIMEOUT = 15

# Capture ball
CPTR_DIST = .3
CPTR_ANGLE = 10

CPTR_SPEED = .4
CPTR_TIME = 2.0

# Hit button
HIT_DIST = .3
HIT_ANGLE = 10

HIT_SPEED = .3
HIT_TIME = 3

# Align Tower
ALIGN_TOWER_PID = (.016, 0, .00, 0.3, 0)
ALIGN_TOWER_DIST = .60
ALIGN_TOWER_ANGLE = 20
ALIGN_TOWER_TRANSLATE_SPEED = 0.3
ALIGN_TOWER_ROTATE_SPEED_SCALE = 0.7

# Rotate in place
ROTINPL_TRANSLATE_SPEED = .10
ROTINPL_ROTATE_SPEED = .12

# Approach target
APP_PID = (.007, 0.0, 0.0, .24, 100)
APP_SPEED = .5
APP_ROTATION = 1.0
APP_SLOWDOWN_DIST = .5

APP_MIN_WHEEL_SPEED = .25
APP_K_WALL_AVOID = 2.0

APP_WALL_SLOWDOWN_DIST = .13
APP_WALL_STOP_DIST = .05

APP_TIMEOUT = 7

# Score
SCORE_DIST = .0
SCORE_TRANSLATE_SPEED = .2
SCORE_ANGLE = 5
NORMAL_RAMP_ANGLE = 40
BLUE_GOAL_RAMP_ANGLE = 110
YELLOW_GOAL_RAMP_ANGLE = 120

# Timeout
TMOUT_TRANSLATE_SPEED = -.4
TMOUT_ROTATE_SPEED = -.3

# Control
RIGHT_MOTOR_MIN = 12
RIGHT_MOTOR_MAX = 127

LEFT_MOTOR_MIN = 12
LEFT_MOTOR_MAX = 127

ROLLER_HELIX_SPEED = 125

ACCEL_LIM = 2.0 #delta per second
