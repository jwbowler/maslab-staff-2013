//comm codes
#define ackCode 0x00
#define setDriveCode 0x01
#define readAnalogCode 0x02

class Motor
{
  private:
    int currentPin, directionPin, pwmPin;
  public:
    Motor(int pPin, int dPin, int cPin)
    {
      currentPin = cPin; // Pin to receive current value (unused in the code)
      directionPin = dPin; // Pin to set motor direction, should be a digital pin, 22-53)
      pwmPin = pPin; // Pin to set motor speed (should be a PWM pin, 2-13)
      pinMode(currentPin, INPUT);
      pinMode(directionPin, OUTPUT);
      pinMode(pwmPin, OUTPUT);
    }
    void setSpeed(int s)
    {
      // Clamp to [-126, 127]
      if (s < -126) s = -126;
      else if (s > 127) s = 127;
      // Scale to [-252, 254]
      s *= 2;
      
      // Set direction and pwm pins
      digitalWrite(directionPin, (s>=0)?HIGH:LOW);
      analogWrite(pwmPin, abs(s));
    }
    int getCurrent() {
      return analogRead(currentPin);
    }
};

Motor *rightMotor;
Motor *leftMotor;

// Special function run when the arduino is first connected to power
void setup()
{
  // Create the serial connection with the eeePC
  Serial.begin(9600);
  Serial.flush();

  leftMotor = new Motor(4,5,0);
  rightMotor = new Motor(6,7,0);
}


int args[4];
char code;
// Special function that is repeatedly called during normal running
// of the Arduino
void loop()
{
  leftMotor->setSpeed(64);
  rightMotor->setSpeed(64);
  Serial.write(analogRead(0));
  
  return;

  // Check if there is any input, otherwise do nothing
  if (Serial.available() > 0)
  {
    code = serialRead();

    switch (code)
    {
      case ackCode:
        Serial.write(0x00);
        break;
      case setDriveCode:
        fillArgs(2);
        leftMotor->setSpeed(args[0]);
        rightMotor->setSpeed(args[1]);
        Serial.write(0x00);
        break;
      case readAnalogCode:
        fillArgs(2);
        Serial.write(analogRead(args[0]));
        break;
    }
  }
}

int argsReceived = 0;
void fillArgs(int num) {
  argsReceived = 0;
  while(argsReceived < num) {
    if(Serial.available() > 0) {
      args[argsReceived++] = Serial.read();
    }
  }
}
