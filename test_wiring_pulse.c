#include "wiring_private.h"
#include "pins_arduino.h"

/* Measures the length (in microseconds) of a pulse on the pin; state is HIGH
 * or LOW, the type of pulse to measure.  Works on pulses from 2-3 microseconds
 * to 3 minutes in length, but must be called at least a few dozen microseconds
 * before the start of the pulse. */
unsigned long pulseIn(uint8_t pin, uint8_t state, unsigned long timeout)
{
	// cache the port and bit of the pin in order to speed up the
	// pulse width measuring loop and achieve finer resolution.  calling
	// digitalRead() instead yields much coarser resolution.
	uint8_t bit = digitalPinToBitMask(pin);
	uint8_t port = digitalPinToPort(pin);
	uint8_t stateMask = (state ? bit : 0);
	unsigned long width = 0; // keep initialization out of time critical area
	
	// convert the timeout from microseconds to a number of times through
	// the initial loop; it takes 16 clock cycles per iteration.
	unsigned long numloops = 0;
	unsigned long maxloops = microsecondsToClockCycles(timeout) / 16;
	
	// wait for any previous pulse to end
	while ((*portInputRegister(port) & bit) == stateMask)
		if (numloops++ == maxloops)
			return 0;
	
	// wait for the pulse to start
	while ((*portInputRegister(port) & bit) != stateMask)
		if (numloops++ == maxloops)
			return 0;
	
	// wait for the pulse to stop
	while ((*portInputRegister(port) & bit) == stateMask) {
		if (numloops++ == maxloops)
			return 0;
		width++;
	}

  //portIn ~= 14? , and, compare, add, compare, add, jmp

	// convert the reading to microseconds. The loop has been determined
	// to be 20 clock cycles long and have about 16 clocks between the edge
	// and the start of the loop. There will be some error introduced by
	// the interrupt handlers.
	return clockCyclesToMicroseconds(width * 21 + 16); 
}


/* Measures the length (in microseconds) of a pulse on the pin; state is HIGH
 * or LOW, the type of pulse to measure.  Works on pulses from 2-3 microseconds
 * to 3 minutes in length, but must be called at least a few dozen microseconds
 * before the start of the pulse. */

void threePulseIn(uint8_t *pin, uint8_t *state, long *times, unsigned long timeout)
{
	uint8_t bit0 = digitalPinToBitMask(pin[0]);
	uint8_t bit1 = digitalPinToBitMask(pin[1]);
	uint8_t bit2 = digitalPinToBitMask(pin[2]);

	uint8_t port0 = digitalPinToPort(pin[0]);
	uint8_t port1 = digitalPinToPort(pin[1]);
	uint8_t port2 = digitalPinToPort(pin[2]);

	uint8_t mask0 = (state[0] ? bit : 0);
	uint8_t mask1 = (state[1] ? bit : 0);
	uint8_t mask2 = (state[2] ? bit : 0);

	unsigned long width0 = 0; // keep initialization out of time critical area
	unsigned long width1 = 0;
	unsigned long width2 = 0;

	uint8_t state0 = 0x04; // keep initialization out of time critical area
	uint8_t state1 = 0x04;
	uint8_t state2 = 0x04;

  uint8_t match0 = 0;
  uint8_t match1 = 0;
  uint8_t match2 = 0;

	// convert the timeout from microseconds to a number of times through
	// the initial loop; it takes 16 clock cycles per iteration.
	unsigned long numloops = 0;
	unsigned long maxloops = microsecondsToClockCycles(timeout) / 16;

  // add, compare, compare, and, or, or ... jmp = 7
  // assign, and, compare, xor, portint ~= 14, and, compare = 20
  // assign, shift = 3
  // assign add and = 3

  // v2 = shared port
  // = 26*3 + 7 = 85 - 28 + 1 = 58 cycles = 3.6 microseconds
  while (numLoops++ < maxLoops && (state0 | state1 | state2)) {
    match0 = (state0 & 0x05 > 0) ^ (*portInputRegister(port0) & bit == mask0)
    state0 >>= match0
    width0 += state0 & 1

    match1 = (state1 & 0x05 > 0) ^ (*portInputRegister(port2) & bit == mask1)
    state1 >>= match1
    width1 += state1 & 1

    match2 = (state2 & 0x05 > 0) ^ (*portInputRegister(port2) & bit == mask2)
    state2 >>= match2
    width2 += state2 & 1
  }

  times[0] = width0;
  times[1] = width1;
  times[2] = width2;

	// convert the reading to microseconds. The loop has been determined
	// to be 20 clock cycles long and have about 16 clocks between the edge
	// and the start of the loop. There will be some error introduced by
	// the interrupt handlers.
	return clockCyclesToMicroseconds(width * 21 + 16); 
}


/* Measures the length (in microseconds) of a pulse on the pin; state is HIGH
 * or LOW, the type of pulse to measure.  Works on pulses from 2-3 microseconds
 * to 3 minutes in length, but must be called at least a few dozen microseconds
 * before the start of the pulse. */
unsigned long pulseIn(uint8_t pin, uint8_t state, unsigned long timeout)
{
	// cache the port and bit of the pin in order to speed up the
	// pulse width measuring loop and achieve finer resolution.  calling
	// digitalRead() instead yields much coarser resolution.
	uint8_t bit = digitalPinToBitMask(pin);
	uint8_t port = digitalPinToPort(pin);
	uint8_t mask = (state ? bit : 0);

	uint8_t state = 0x04;
  uint8_t match = 0;

	unsigned long width = 0; // keep initialization out of time critical area


	
	// convert the timeout from microseconds to a number of times through
	// the initial loop; it takes 16 clock cycles per iteration.
	unsigned long numloops = 0;
	unsigned long maxloops = microsecondsToClockCycles(timeout) / 16;

  //inc, cmp, and, jmp = 4
  //ass, and, cmp, xor, port=14, and, cmp = 20
  //ass, shift = 2
  //ass, add, and = 2
  //total = 28
  while ((numLoops++ < maxLoops) && state0) {
    match0 = (state0 & 0x05 > 0) ^ (*portInputRegister(port0) & bit == mask0)
    state0 >>= match0
    width0 += (state0 & 1)
  }

  //was 20 loop + 16 pre-loop
  //now 28 loop + 20 pre-loop?
	return clockCyclesToMicroseconds(width * 28 + 20); 
}
