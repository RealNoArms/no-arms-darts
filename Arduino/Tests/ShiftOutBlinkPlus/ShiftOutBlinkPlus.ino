/*
  ShiftOutBlinkPlus
  
  Builds on the original Blink and Shiftout examples with 
    patterns for 4 LEDs

  Blinks each LED on and off 4 times, then flips it to negative
    and blinks each off an on 

  This example code is in the public domain.
*/

//Pin connected to latch pin (ST_CP) of 74HC595
const int latchPin = 3;
//Pin connected to clock pin (SH_CP) of 74HC595
const int clockPin = 2;
////Pin connected to Data in (DS) of 74HC595
const int dataPin = 7;

// control variables
int delayCount = 500;
int repeatCount = 4;

byte pos = 1;
byte neg = 0;

byte pattern = 0;

// the setup routine runs once when you press reset:
void setup() {     
  //set pins to output so you can control the shift register
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
}

void setPos(byte posVal)
{
  pos = posVal;
  if (pos == 1)
  {
    neg = 0;
  }
  else
  {
    neg = 1;
  } 
}

// blink the given bit on then off
void blinkoUno(int ledNum) {
  bitWrite(pattern, ledNum, pos);
  displayPattern();
  delay(delayCount);
  
  bitWrite(pattern, ledNum, neg);
  displayPattern();
  delay(delayCount);
}

// the loop routine runs over and over again forever:
void loop() {
  
  reset();
  delay(delayCount*2);
  
  for (int i=0; i < 4; i++)
  {
    for (int j=0; j < repeatCount; j++)
    {
      blinkoUno(i);
    }
  }
  
  // toggle negative
  setPos(neg);
}


// sends the given byte to the shift register
void displayPattern() {

  // take the latchPin low so 
  // the LEDs don't change while you're sending in bits:
  digitalWrite(latchPin, LOW);
  
  // shift out the bits:
  shiftOut(dataPin, clockPin, MSBFIRST, pattern);
  
  //take the latch pin high so the LEDs will light up:
  digitalWrite(latchPin, HIGH);
}

// sets all bits to off
void reset() {
  if (pos == 1)
  {
    pattern = 0;
  }
  else
  {
    pattern = ~0;
  }
  
  displayPattern();
}


