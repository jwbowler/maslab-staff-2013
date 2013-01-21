#include "wiring_private.h"
#include "pins_arduino.h"

/* Measures the length (in microseconds) of a pulse on the pin; state is HIGH
 * or LOW, the type of pulse to measure.  Works on pulses from 2-3 microseconds
 * to 3 minutes in length, but must be called at least a few dozen microseconds
 * before the start of the pulse. */
unsigned long newPulseIn(uint8_t pin, uint8_t state, unsigned long timeout)
{
	// cache the port and bit of the pin in order to speed up the
	// pulse width measuring loop and achieve finer resolution.  calling
	// digitalRead() instead yields much coarser resolution.
	uint8_t bit = digitalPinToBitMask(pin);
	uint8_t port = digitalPinToPort(pin);
	uint8_t mask = (state ? bit : 0);

	uint8_t iter = 0x04;
  uint8_t match = 0;

	unsigned long width = 0; // keep initialization out of time critical area


	
	// convert the timeout from microseconds to a number of times through
	// the initial loop; it takes 16 clock cycles per iteration.
	unsigned long numloops = 0;
	unsigned long maxloops = microsecondsToClockCycles(timeout) / 28;

  //inc, cmp, and, jmp = 4
  //ass, and, cmp, xor, port=14, and, cmp = 20
  //ass, shift = 2
  //ass, add, and = 2
  //total = 28
  while ((numloops++ < maxloops) && iter) {
    match = (iter & 0x05 > 0) ^ (*portInputRegister(port) & bit == mask);
    iter >>= match;
    width += (iter & 1);
  }

  //was 20 loop + 16 pre-loop
  //now 28 loop + 20 pre-loop?
	return clockCyclesToMicroseconds(width * 28 + 20); 
}

void setup() {
  Serial.begin(9600);
}

void loop()
{
  digitalWrite(2, HIGH);
  // establish variables for duration of the ping,
  // and the dirtance result in inches and centimeters:
  long duration;
  double cm;

  // The PING))) is triggered by a HIGH pulse of 2 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  pinMode(14, OUTPUT);// attach pin 3 to Trig
  digitalWrite(14, LOW);
  delayMicroseconds(2);
  digitalWrite(14, HIGH);
  delayMicroseconds(5);
  digitalWrite(14, LOW);

  // The same pin is used to read the signal from the PING))): a HIGH
  // pulse whose duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  pinMode (15, INPUT);//attach pin 4 to Echo
  duration = newPulseIn(15, HIGH, 6000);

  // convert the time into a distance
  cm = microsecondsToCentimeters(duration);
 
  Serial.print("dur: ");
  Serial.println(duration);
  Serial.print(cm);
  Serial.print("cm");
  Serial.println();
 
  delay(100);
}

double microsecondsToCentimeters(long microseconds)
{
  // The speed of sound is 340 m/s or 29 microseconds per centimeter.
  // The ping travels out and back, so to find the distance of the
  // object we take half of the distance travelled.
  return microseconds / 29.0 / 2.0;
}
