#Commander
LOG_FREQUENCY = .5 #seconds

TIME_BEFORE_HALT = -1 # value <= 0 --> never stops
BALL_BUTTON_TIMEOUT = 20

#Pins
IR_PINS = []
ULT_PINS =[(52,53),(50,51),(48,49),(46,47)]

COLOR_SWITCH_PIN = 11
RESET_BUTTON_PIN = 12

LEFT_MOTOR_PINS = (14,2,3)
RIGHT_MOTOR_PINS = (15,4,5)
ROLLER_PINS = (13,13,6)
HELIX_PINS = (13,13,7)
RAMP_SERVO_PIN = 8
SCORER_PIN = 12

#Data Collection
IR_POSITIONS = []

ULT_POSITIONS = [(.14,-108),(.14,-72),(.13,-36),(.10,0)]
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
MIN_WAIT_BETWEEN_SCORING = 5
ONLY_SCORE_PERIOD = 30

#Movement
# Follow wall
WF_DIST_PID = (0.6, 0, .000, 0.35, 0)
WF_ANGLE_PID = (.02, 0, .0, 0.35, 0)

WF_SLOWDOWN_DIST = .22
WF_STOP_DIST = .03

WF_ROT_LIM = .5
WF_DIST_TARGET = .35
WF_SPEED = .0 #.4
WF_ROTATION = 1.0

# Capture ball
CPTR_DIST = .3
CPTR_ANGLE = 10

CPTR_SPEED = .3
CPTR_TIME = 2

# Hit button
HIT_DIST = .3
HIT_ANGLE = 10

HIT_SPEED = .3
HIT_TIME = 3

# Align Tower
ALIGN_TOWER_PID = (.016, 0, .02, 0.3, 0)
ALIGN_TOWER_DIST = .5
ALIGN_TOWER_ANGLE = 15
ALIGN_TOWER_TRANSLATE_SPEED = 0.1
ALIGN_TOWER_ROTATE_SPEED_SCALE = 0.5

# Rotate in place
ROTINPL_TRANSLATE_SPEED = .10
ROTINPL_ROTATE_SPEED = .12

# Approach target
APP_PID = (.03, 0.0, 0.0, .2, 100)
APP_SPEED = .4
APP_ROTATION = 1.0
APP_SLOWDOWN_DIST = .5

# Score
SCORE_DIST = .50
SCORE_ANGLE = 5

# Timeout
TMOUT_TRANSLATE_SPEED = -.4
TMOUT_ROTATE_SPEED = -.3

#Control
RIGHT_MOTOR_MIN = 8
RIGHT_MOTOR_MAX = 127

LEFT_MOTOR_MIN = 8
LEFT_MOTOR_MAX = 127

ROLLER_SPEED=050
HELIX_SPEED=060

ACCEL_LIM = 2.0 #delta per second
