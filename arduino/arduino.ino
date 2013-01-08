#include <SoftareSerial.h>
#include <Servo.h>

//codes
#define liveCode 0x00
#define moveCode 0x01

#define leftMotorDirPin 0
#define leftMotorPwnPin 0
#define leftMotorCurPin 0

#define rightMotorDirPin 0
#define rightMotorPwnPin 0
#define rightMotorCurPin 0

#define irPin 0

/*
struct Motor {
  int dirPin;
  int pwmPin;
  int curPint;
}

Motor rightMotor;
Motor leftMotor;
*/

void setMotor(int dirPin, int pwmPin, int dir, int pwm) {
  if (pwm < 0) pwm = 0;
  else if (pwm > 255) pwm = 255;
  
  digitalWrite(dirPin, (dir>=0)?HIGH:LOW);
  analogWrite(pwmPin, pwm);
}

// Define a serial read that actually blocks
char serialRead()
{
  char in;
  // Loop until input is not -1 (which means no input was available)
  while ((in = Serial.read()) == -1) {}
  return in;
}

// Special function run when the arduino is first connected to power
void setup()
{
  // Create the serial connection with the eeePC
  Serial.begin(9600);
  // Clear the buffer
  Serial.flush();

  //pin modes for left motor
  pinMode(leftMotorCurPin, INPUT);
  pinMode(leftMotorDirPin, OUTPUT);
  pinMode(leftMotorPwnPin, OUTPUT);
  
  //pin modes for left motor
  pinMode(rightMotorCurPin, INPUT);
  pinMode(rightMotorDirPin, OUTPUT);
  pinMode(rightMotorPwnPin, OUTPUT);
}


// Special function that is repeatedly called during normal running
// of the Arduino
void loop()
{
  setMotor(leftMotorDirPin, leftMotorPwnPin, 1, 64);
  setMotor(rightMotorDirPin, rightMotorPwnPin, 1, 64);

  Serial.write(analogRead(irPin));
  
  return;

  // Check if there is any input, otherwise do nothing
  int in;
  while ((in = Serial.read()) == -1) {}
  if (Serial.available() > 0)
  {
    char mode = serialRead();

    switch (mode)
    {
      //setMotors();
      break;
    }
  }
}
