/*
  BlinkPlus
  
  Builds on the original Blink example with patterns for 4 LEDs
  LEDs are wired (through a resistor) to Arduino digital ports
    8,9,10 and 11
  
  Defaults to run westinghouseSign() in the main loop
  westinghouseSign() randomly sets the delay, repeat and LED pattern
  http://en.wikipedia.org/wiki/Westinghouse_Sign

  This example code is in the public domain.
 */

// constants
const int MIN_DELAY = 50;
const int MAX_DELAY = 1000;

const int MIN_REPEAT = 1;
const int MAX_REPEAT = 5;

const int NUM_PATTERNS = 13;

// 4 pins for 4 LEDs
int led[4] = {8,9,10,11};

// control variables
int delayCount = 100;
int repeatCount = 8;
int negative = LOW;
int positive = HIGH;

// the setup routine runs once when you press reset:
void setup() {                
  // initialize the digital pins as a outputs.
  for (int i=0; i<4; i++)
  {
    pinMode(led[i], OUTPUT);
  }
  
  // seed the "random" number generator
  randomSeed(analogRead(0));
}

void setPositive(int pos) {
  if (pos == LOW)
  {
    negative = HIGH;
    positive = LOW;
  }
  else if (pos == HIGH)
  {
    positive = HIGH;
    negative = LOW;
  }
}

// the loop routine runs over and over again forever:
void loop() {
  westinghouseSign();
}

void westinghouseSign() {
  // get random delay
  delayCount = random(MIN_DELAY, MAX_DELAY+1);
  
  // get random repeat
  repeatCount = random(MIN_REPEAT, MAX_REPEAT+1);
  
  // get random positive setting
  if (random(0,2) == 0)
  {
    setPositive(HIGH);
  }
  else
  {
    setPositive(LOW);
  }
  
  // do a reset
  reset();
  
  // get random pattern id
  int patternId = random(0, NUM_PATTERNS);
  
  for (int i=0; i < repeatCount; i++)
  {
    switch (patternId)
    {
      case(0):
        blinkoUno(random(0,4));
        break;
        
      case(1):
        ascendOnce();
        break;
        
      case(2):
        descendOnce();
        break;
        
      case(3):
        quadraBlink();
        break;
        
      case(4):
        wipeUnwipe();
        break;
        
      case(5):
        epiwnUepiw();
        break;
        
      case(6):
        wipePong();
        break;
        
      case(7):
        knightRider();
        break;
        
      case(8):
        pingPong();
        break;
        
      case(9):
        eitherOr();
        break;
        
      case(10):
        innerOuter();
        break;
        
      case(11):
        noahsArk();
        break;
        
      case(12):
        noahsReturn();
        break;
        
      default:
        blinkoUno(random(0,4));
    }
  }
}

void reset() {
    for (int j=0; j<4; j++)
    {
      digitalWrite(led[j], negative);    // turn the LED off by making the voltage LOW
    }
}

void blinkoUno(int ledNum) {
  digitalWrite(led[ledNum], positive);   // turn the LED on (HIGH is the voltage level)
  delay(delayCount);            // wait for delay count
  digitalWrite(led[ledNum], negative);   // turn the LED on (HIGH is the voltage level)
  delay(delayCount);            // wait for delay count
}

void ascendOnce() {
    for (int j=0; j<4; j++)
    {
      digitalWrite(led[j], positive);   // turn the LED on (HIGH is the voltage level)
      delay(delayCount);            // wait for delay count
      digitalWrite(led[j], negative);    // turn the LED off by making the voltage LOW
    }
}

void descendOnce() {
    for (int j=4; j>0; j--)
    {
      digitalWrite(led[j-1], positive);   // turn the LED on (HIGH is the voltage level)
      delay(delayCount);             // wait for delay count
      digitalWrite(led[j-1], negative);    // turn the LED off by making the voltage LOW
    }
}

void quadraBlink() {
  setPositive(LOW);
  reset();
  delay(delayCount);             // wait for delay count
  setPositive(HIGH);
  reset();
  delay(delayCount);             // wait for delay count
}

void wipeUnwipe() {
  setPositive(LOW);
  ascendOnce();
  setPositive(HIGH);
  ascendOnce();
}

void epiwnUepiw() {
  setPositive(LOW);
  descendOnce();
  setPositive(HIGH);
  descendOnce();
}

void wipePong() {
  wipeUnwipe();
  epiwnUepiw();
}

void knightRider() {
  ascendOnce();
  descendOnce();
}

void pingPong() {
  ascendOnce();
    for (int j=3; j>1; j--)
    {
      digitalWrite(led[j-1], positive);   // turn the LED on (HIGH is the voltage level)
      delay(delayCount);             // wait for delay count
      digitalWrite(led[j-1], negative);    // turn the LED off by making the voltage LOW
    }
}

void eitherOr() {
  digitalWrite(led[1], negative);
  digitalWrite(led[3], negative);
  digitalWrite(led[0], positive);
  digitalWrite(led[2], positive);
  delay(delayCount); 
  digitalWrite(led[0], negative);
  digitalWrite(led[2], negative);
  digitalWrite(led[1], positive);
  digitalWrite(led[3], positive);
  delay(delayCount); 
}

void innerOuter() {
  digitalWrite(led[0], negative);
  digitalWrite(led[3], negative);
  digitalWrite(led[1], positive);
  digitalWrite(led[2], positive);
  delay(delayCount); 
  digitalWrite(led[1], negative);
  digitalWrite(led[2], negative);
  digitalWrite(led[0], positive);
  digitalWrite(led[3], positive);
  delay(delayCount); 
}

void noahsArk() {
  digitalWrite(led[0], positive);
  digitalWrite(led[1], negative);
  digitalWrite(led[2], negative);
  digitalWrite(led[3], negative);
  delay(delayCount); 
  digitalWrite(led[0], positive);
  digitalWrite(led[1], positive);
  digitalWrite(led[2], negative);
  digitalWrite(led[3], negative);
  delay(delayCount); 
  digitalWrite(led[0], negative);
  digitalWrite(led[1], positive);
  digitalWrite(led[2], positive);
  digitalWrite(led[3], negative);
  delay(delayCount); 
  digitalWrite(led[0], negative);
  digitalWrite(led[1], negative);
  digitalWrite(led[2], positive);
  digitalWrite(led[3], positive);
  delay(delayCount); 
  digitalWrite(led[0], negative);
  digitalWrite(led[1], negative);
  digitalWrite(led[2], negative);
  digitalWrite(led[3], positive);
  delay(delayCount); 
}

void noahsReturn() {
  digitalWrite(led[0], negative);
  digitalWrite(led[1], negative);
  digitalWrite(led[2], negative);
  digitalWrite(led[3], positive);
  delay(delayCount); 
  digitalWrite(led[0], negative);
  digitalWrite(led[1], negative);
  digitalWrite(led[2], positive);
  digitalWrite(led[3], positive);
  delay(delayCount); 
  digitalWrite(led[0], negative);
  digitalWrite(led[1], positive);
  digitalWrite(led[2], positive);
  digitalWrite(led[3], negative);
  delay(delayCount); 
  digitalWrite(led[0], positive);
  digitalWrite(led[1], positive);
  digitalWrite(led[2], negative);
  digitalWrite(led[3], negative);
  delay(delayCount); 
  digitalWrite(led[0], positive);
  digitalWrite(led[1], negative);
  digitalWrite(led[2], negative);
  digitalWrite(led[3], negative);
  delay(delayCount); 
}
