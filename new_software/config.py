# Game variables
MY_BALLS_ARE_RED = True
TIME_BEFORE_HALT = -1 # value <= 0 --> never stops

# Robot properties
ROBOT_RADIUS = .17

# Sensors
IR_PINS = (13,14,15)
IR_POSITIONS = [(.15, -85),(.15, 0),(.15, 85)]

ULT_PINS =[(14,15),(18,19)]
ULT_POSITIONS = [(.15,-40), (.15, 40)]

MOTOR_CURRENT_PINS = (0,0,0,0)

BALL_IN_SENSOR_PIN = 0
BALL_OUT_SENSOR_PIN = 0

# Motors (current, dir, pwm)
ROLLER_PINS = (11,3,4)
RIGHT_MOTOR_PINS = (11,5,6)
LEFT_MOTOR_PINS = (11,9,10)
HELIX_PINS = (11,7,8)
RAMP_SERVO_PIN = 0
SCORER_PIN=0

# Control
RIGHT_MOTOR_MIN = 8
RIGHT_MOTOR_MAX = 127

LEFT_MOTOR_MIN = 8
LEFT_MOTOR_MAX = 127

ROLLER_SPEED=-80
HELIX_SPEED=0

