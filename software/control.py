import arduino
import pid

class Control:
  def __init__(self, arduino)
    self.ard = arduino

  def initMotors():
    motors[] = []
    
    self.motors[0] = arduino.Motor(ard, 10, 5, 3)
    self.motors[1] = arduino.Motor(ard, 10, 6, 4)
