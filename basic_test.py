import arduino

ard = arduino.Arduino()
r = arduino.Motor(ard, 11, 5, 6)
l = arduino.Motor(ard, 11, 9, 10)
f = arduino.Motor(ard, 11, 3, 4)
ard.run()

r.setSpeed(50)
l.setSpeed(50)
f.setSpeed(50)

