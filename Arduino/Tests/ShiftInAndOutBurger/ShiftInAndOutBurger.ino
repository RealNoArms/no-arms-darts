/*
  ShiftInAndOutBurger
  
  Adds a shiftIn to the ShiftOutBlinkPlus to use the
  parallel inputs of the 74HC589 parallel to serial
  shift register instead of software inputs.

  This example code is in the public domain.
*/

//////////////////////////////////////////////////////////////
//  Variable Declarations
//////////////////////////////////////////////////////////////

//Pin connected to latch pin (ST_CP) of 74HC595
const int latchPin_out = 3;
//Pin connected to clock pin (SH_CP) of 74HC595
const int clockPin_out = 2;
////Pin connected to Data in (DS) of 74HC595
const int dataPin_out = 7;

////Pin connected to parallel load pin of 74HC589
const int loadPin_in = 8;
//Pin connected to latch clock pin of 74HC589
const int latchPin_in = 9;
//Pin connected to shift clock pin of 74HC589
const int clockPin_in = 10;
////Pin connected to Data out (QW/QH?) of 74HC589
const int dataPin_in = 11;


//////////////////////////////////////////////////////////////
//  Main
//////////////////////////////////////////////////////////////

// the setup routine runs once when you press reset:
void setup() {     
  //set pins to output so you can control the 74HC595
  pinMode(latchPin_out, OUTPUT);
  pinMode(clockPin_out, OUTPUT);
  pinMode(dataPin_out, OUTPUT);
  
  //set pins to output so you can read from the 74HC589
  pinMode(loadPin_in, OUTPUT);
  pinMode(latchPin_in, OUTPUT);
  pinMode(clockPin_in, OUTPUT);
  pinMode(dataPin_in, INPUT);
  
  // set latch pin IN to low and load pin to high initially
  digitalWrite(latchPin_in, LOW);
  digitalWrite(loadPin_in, HIGH);
  
  /* DEBUG */
  Serial.begin(9600);
  Serial.println("start");
  Serial.println("");
  /**/
}

// the loop routine runs over and over again forever:
void loop() {
  
  // move latch from LOW to HIGH to move parallel inputs to data latch
  digitalWrite(latchPin_in, HIGH);
  
  // reset the latch
  digitalWrite(latchPin_in, LOW);
  
  // move the load pin from high to low move the data from the data latch 
  //to the shift registers
  digitalWrite(loadPin_in, LOW);
  
  // move load pin from low to high to enable shifting
  digitalWrite(loadPin_in, HIGH);
  
  // shift the data in from the 74HC589 to a byte variable
  byte pattern = naShiftIn(dataPin_in, clockPin_in, MSBFIRST);
  
  /* DEBUG */
  Serial.println("byte value:");
  Serial.println(pattern);
  Serial.println("");
  /**/
  
  // send the byte out to the 74HC595
  displayPattern(pattern);
  
  // wait 5 seconds and do it again
  delay(5000);
}

// replaces built-in shiftIn to read the first bit before pulsing the clock
uint8_t naShiftIn(uint8_t dataPin, uint8_t clockPin, uint8_t bitOrder) {
	uint8_t value = 0;
	uint8_t i;

	for (i = 0; i < 8; ++i) {
		if (bitOrder == LSBFIRST)
			value |= digitalRead(dataPin) << i;
		else
			value |= digitalRead(dataPin) << (7 - i);

		digitalWrite(clockPin, HIGH);
		digitalWrite(clockPin, LOW);
	}
	return value;
}

// sends the pattern byte to the 74HC595
void displayPattern(byte pattern) {

  // take the latchPin low so 
  // the LEDs don't change while you're sending in bits:
  digitalWrite(latchPin_out, LOW);
  
  // shift out the bits:
  shiftOut(dataPin_out, clockPin_out, MSBFIRST, pattern);
  
  //take the latch pin high so the LEDs will light up:
  digitalWrite(latchPin_out, HIGH);
}
