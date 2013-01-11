import arduino

class DataCollection:
  def __init__(self, arduino):
    self.ard = arduino

  def initSensors():
    self.infra = []
    self.bump = []
    self.encoders = []

    self.infra[0] = arduino.AnalogInput(self.ard, 1)
    self.infra[1] = arduino.AnalogInput(self.ard, 2)
    self.infra[2] = arduino.AnalogInput(self.ard, 3)

    self.bump[0] = arduino.DigitalInput(self.ard, 1)
    self.bump[1] = arduino.DigitalInput(self.ard, 2)
    self.bump[2] = arduino.DigitalInput(self.ard, 3)

  def sample():

