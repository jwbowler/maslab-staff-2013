# Game variables
MY_BALLS_ARE_RED = True
TIME_BEFORE_HALT = -1 # value <= 0 --> never stops

# Robot properties
ROBOT_RADIUS

# Sensors
IR_PINS = (0,0,0,0,0)
# (distance from center, angle from front)
IR_POSITIONS = ((0,0),(0,0),(0,0),(0,0),(0,0))
ULTRASONIC_PINS =(0,0,0)
MOTOR_CURRENT_PINS = (0,0,0,0)
BALL_IN_SENSOR_PIN = 0
BALL_OUT_SENSOR_PIN = 0

# Motors (current, dir,pwn)
ROLLER_PINS = (0,0,0)
RIGHT_MOTOR_PINS = (0,0,0)
LEFT_MOTOR_PINS = (0,0,0)
HELIX_PINS = (0,0,0)
RAMP_SERVO_PIN = 0
SCORER_PIN=0

# Control
RIGHT_MOTOR_MIN = 8
RIGHT_MOTOR_MAX = 127

LEFT_MOTOR_MIN = 8
LEFT_MOTOR_MAX = 127

ROLLER_SPEED=0
HELIX_SPEED=0

