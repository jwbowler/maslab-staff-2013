#Debugging
LOG_FREQUENCY = .1 #seconds

# Game variables
MY_BALLS_ARE_RED = False 
TIME_BEFORE_HALT = 180 # value <= 0 --> never stops
BALL_BUTTON_TIMEOUT = 20

# Strategy
MIN_WAIT_BETWEEN_SCORING = 5
ONLY_SCORE_PERIOD = 30

# Dimensions
ROBOT_RADIUS = .17
BALL_RADIUS = .02
BUTTON_CENTER_HEIGHT = .075
YELLOW_WALL_CENTER_HEIGHT = 0.06 # not counting blue stripe
TOWER_BASE_CENTER_HEIGHT = .075
TOWER_TOP_CENTER_HEIGHT = .27

# Sensors
IR_PINS = []
IR_POSITIONS = []

#ULT_PINS =[(22,23),(24,25),(26,27),(28,29)]
#ULT_POSITIONS = [(.16,-108), (.15, -72), (.14, -36), (.15, 0)]
ULT_PINS =[(52,53),(50,51),(48,49),(46,47)]
ULT_POSITIONS = [(.14,-108),(.14,-72),(.13,-36),(.10,0)]
ULT_TIMEOUT = 6000
MOTOR_CURRENT_PINS = (0,0,0,0)

BALL_IN_SENSOR_PIN = 0
BALL_OUT_SENSOR_PIN = 0

# Motors (current, dir, pwm)
LEFT_MOTOR_PINS = (14,2,3)
RIGHT_MOTOR_PINS = (15,4,5)
ROLLER_PINS = (13,6,7)
HELIX_PINS = (13,8,9)
RAMP_SERVO_PIN = 14
SCORER_PIN = 15

# Control
RIGHT_MOTOR_MIN = 8
RIGHT_MOTOR_MAX = 127

LEFT_MOTOR_MIN = 8
LEFT_MOTOR_MAX = 127

ROLLER_SPEED=-80
HELIX_SPEED=50

# MOVEMENT CONSTANTS

# Capture ball
CPTRBL_TRANSLATE_SPEED = .3
CPTRBL_ROTATE_SPEED = 0

# Hit button
HITBTN_TRANSLATE_SPEED = .3
HITBTN_ROTATE_SPEED = 0

# Align
ALIGN_ROTATE_SPEED_SCALE = 0.4

# Rotate in place
ROTINPL_TRANSLATE_SPEED = .10
ROTINPL_ROTATE_SPEED = .12

# Approach target
APPTGT_TRANSLATE_SPEED = .3
APPTGT_ROTATE_SPEED = .2

# Avoid wall
AVDWLL_TRANSLATE_SPEED = -.3
AVDWLL_ROTATE_SPEED = -0.2

# Follow wall
FW_PHI = 18
FW_DIST_TARGET = .25
FW_TRANSLATE_SPEED = .2
FW_ROTATE_SPEED_SCALE = 1


