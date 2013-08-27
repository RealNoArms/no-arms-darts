/*
  ShiftInAndBasic
  
  Basic test of the74HC589 parallel to serial
  shift register.

  This example code is in the public domain.
*/

//////////////////////////////////////////////////////////////
//  Variable Declarations
//////////////////////////////////////////////////////////////


////Pin connected to parallel load pin of 74HC589
const int loadPin_in = 8;
//Pin connected to latch clock pin of 74HC589
const int latchPin_in = 9;
//Pin connected to shift clock pin of 74HC589
const int clockPin_in = 10;
////Pin connected to Data out (QH) of 74HC589
const int dataPin_in = 11;


//////////////////////////////////////////////////////////////
//  Main
//////////////////////////////////////////////////////////////

// the setup routine runs once when you press reset:
void setup() {     
  
  //set pins to output so you can read from the 74HC589
  pinMode(loadPin_in, OUTPUT);
  pinMode(latchPin_in, OUTPUT);
  pinMode(clockPin_in, OUTPUT);
  pinMode(dataPin_in, INPUT);
  
  // set latch pin IN to low and load pin to high initially
  digitalWrite(latchPin_in, LOW);
  digitalWrite(loadPin_in, HIGH);

  Serial.begin(9600);
  Serial.println("start");
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
  digitalWrite(loadPin_in, HIGH);   // AAAAARRRRRRRGGGGHHHHHH!
  
  Serial.println("shifting in...");
  
  // shift the data in from the 74HC589 to a byte variable
  byte pattern = naShiftIn(dataPin_in, clockPin_in, MSBFIRST);
  

  Serial.println("byte value:");
  Serial.println(pattern);
  Serial.println("");
    
  // wait 3 seconds
  delay(3000);
  
  /*Serial.println(latchPin_in); 
  Serial.println("digitalWrite(latchPin_in, HIGH);");  
  digitalWrite(latchPin_in, HIGH);
  
  delay(5000);
  Serial.println(latchPin_in);
  Serial.println("digitalWrite(latchPin_in, LOW);");  
  digitalWrite(latchPin_in, LOW);
  
  delay(5000);
  
    Serial.println(loadPin_in);
  Serial.println("digitalWrite(loadPin_in, HIGH);");  
  digitalWrite(loadPin_in, HIGH);
  
  delay(5000);
  Serial.println(loadPin_in);
  Serial.println("digitalWrite(loadPin_in, LOW);");  
  digitalWrite(loadPin_in, LOW);
  
  delay(5000);
  
  Serial.println(clockPin_in);
  Serial.println("digitalWrite(clockPin_in, HIGH);");  
  digitalWrite(clockPin_in, HIGH);
  
  delay(5000);
  Serial.println(clockPin_in);
  Serial.println("digitalWrite(clockPin_in, LOW);");  
  digitalWrite(clockPin_in, LOW);
  
  delay(5000);*/

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

