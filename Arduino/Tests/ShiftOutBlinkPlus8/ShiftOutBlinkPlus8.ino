/*
  ShiftOutBlinkPlus8
  
  Builds on the original Blink and Shiftout examples with 
    patterns for 8 LEDs

  Defaults to run westinghouseSign() in the main loop
  westinghouseSign() randomly sets the delay, repeat and pattern
  http://en.wikipedia.org/wiki/Westinghouse_Sign

  This example code is in the public domain.
*/

//////////////////////////////////////////////////////////////
//  PatternGenerator Ids
//////////////////////////////////////////////////////////////

#define BLINKO_UNO           0
#define ASCEND_ONCE          1
#define DESCEND_ONCE         2
#define KINGHTRIDER          3
#define PING_PONG            4
#define WIPE_UNWIPE          5
#define EPIWN_UWEPIW         6
#define WIPE_PONG            7
#define QUADRA_BLINK         8
#define EITHER_OR            9
#define INNER_OUTER          10
#define NOAHS_ARK            11
#define NOAHS_RETURN         12

#define FIRST_PATTERN        BLINKO_UNO
#define LAST_PATTERN         NOAHS_RETURN

#define MIN_DELAY            50
#define MAX_DELAY            500

#define MIN_REPEATS          4
#define MAX_REPEATS          8

//////////////////////////////////////////////////////////////
//  Variable Declarations
//////////////////////////////////////////////////////////////

//Pin connected to latch pin (ST_CP) of 74HC595
const int latchPin = 11;
//Pin connected to clock pin (SH_CP) of 74HC595
const int clockPin = 12;
////Pin connected to Data in (DS) of 74HC595
const int dataPin = 2;

// control variables
int delayCount = 100;
int repeatCount = 4;

byte pos = 1;
byte neg = 0;

byte pattern = 0;


//////////////////////////////////////////////////////////////
//  Main
//////////////////////////////////////////////////////////////

// the setup routine runs once when you press reset:
void setup() {     
  //set pins to output so you can control the shift register
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  
  // seed the "random" number generator
  randomSeed(analogRead(0));
}

// the loop routine runs over and over again forever:
void loop() {
   testAll();
  //westinghouseSign();
}

//////////////////////////////////////////////////////////////
//  Pattern Managers
//////////////////////////////////////////////////////////////

// Runs through all pattern generators once, then again in the negative
void testAll() {
  
  // to test a single pattern generator:
  // for (int p = NEW_PATTERN; p <= NEW_PATTERN; p++)
  
  // loop through all pattern generators
  for (int p = FIRST_PATTERN; p <= LAST_PATTERN; p++)
  {
    reset();
    delay(delayCount*2);
    
    if (p == BLINKO_UNO)
    {
      // blink each LED
      for (int i=0; i < 8; i++)
      {
        for (int j=0; j < repeatCount; j++)
        {
          runPatternGenerator(p, i);
        }
      }
    }
    else
    {
      for (int i=0; i < repeatCount; i++)
      {
        runPatternGenerator(p);
      }
    }
  }
  
  // toggle negative
  setPos(neg);
}

// random patterns, repeats and delays
void westinghouseSign() {
  // get random delay
  delayCount = random(MIN_DELAY, MAX_DELAY+1);
  
  // get random repeat
  repeatCount = random(MIN_REPEATS, MAX_REPEATS+1);
  
  // get random positive setting
  setPos(random(0,2));
  
  // do a reset
  reset();
  
  for (int i=0; i < repeatCount; i++)
  {
    // send a random patternId and ledNumber
    runPatternGenerator(random(FIRST_PATTERN, LAST_PATTERN+1), random(0, 8));
  }
}

//////////////////////////////////////////////////////////////
//  Helper Methods
//////////////////////////////////////////////////////////////

// runs the given pattern generator (with a default LED number parameter)
void runPatternGenerator(int patternId) {
  runPatternGenerator(patternId, 0);
}

// runs the given pattern generator, using the given LED number where applicable
void runPatternGenerator(int patternId, int ledNumber) {
    switch (patternId)
    {
      case(BLINKO_UNO):
        blinkoUno(ledNumber);
        break;
        
      case(ASCEND_ONCE):
        ascendOnce();
        break;
        
      case(DESCEND_ONCE):
        descendOnce();
        break;
        
      case(KINGHTRIDER):
        knightRider();
        break;
        
      case(PING_PONG):
        pingPong();
        break;
        
      case(WIPE_UNWIPE):
        wipeUnwipe();
        break;
        
      case(EPIWN_UWEPIW):
        epiwnUepiw();
        break;
        
      case(WIPE_PONG):
        wipePong();
        break;
        
      case(QUADRA_BLINK):
        quadraBlink();
        break;
        
      case(EITHER_OR):
        eitherOr();
        break;
        
      case(INNER_OUTER):
        innerOuter();
        break;
        
      case(NOAHS_ARK):
        noahsArk();
        break;
        
      case(NOAHS_RETURN):
        noahsReturn();
        break;
        
      default:
        blinkoUno(ledNumber);
    }
}

// sends the pattern byte to the shift register
void displayPattern() {

  // take the latchPin low so 
  // the LEDs don't change while you're sending in bits:
  digitalWrite(latchPin, LOW);
  
  // shift out the bits:
  shiftOut(dataPin, clockPin, MSBFIRST, pattern);
  
  //take the latch pin high so the LEDs will light up:
  digitalWrite(latchPin, HIGH);
}

// sets all bits to neg
void reset() {
  if (pos == 1)
  {
    pattern = 0;
  }
  else
  {
    pattern = 255;
  }
  
  displayPattern();
}

// sets pos to either ON or OFF
// OFF renders the pattern as a negative
void setPos(byte posVal)
{
  pos = posVal;
  neg = !pos;
}

// return positive or negative pattern according to
// negation settings
byte posNegPattern(byte pattern) { 
  if (neg)
  {
    pattern = ~pattern;
  }
  return pattern;
}

//////////////////////////////////////////////////////////////
// Pattern Generators
//////////////////////////////////////////////////////////////

// blink the given bit on then off
void blinkoUno(int ledNum) {
  bitWrite(pattern, ledNum, pos);
  displayPattern();
  delay(delayCount);
  
  bitWrite(pattern, ledNum, neg);
  displayPattern();
  delay(delayCount);
}

// turning each bit on then off in sequence
void ascendOnce() {
  // loop through all 8 LEDs (+1)
  for (int i=0; i<=8; i++)
  {
    if (i != 0)
    {
      // turn the previous LED off (unless we're on the first one)
      bitWrite(pattern, i-1, neg);
    }
    if (i != 8)
    {
      // turn the current LED on (unless past the last one)
      bitWrite(pattern, i, pos);
    }
    
    displayPattern();
    
    // Don't delay after the last display, for more fluid transitions
    if (i != 8)
    {
      delay(delayCount);
    }
  }
}

// turn each bit on then off in reverse sequence
void descendOnce() {
  // start with the last LED
  int j = 7;
  
  // loop through all 4 LEDs (+1)
  for (int i=0; i<=8; i++)
  {
    if (i != 0)
    {
      // turn the previous LED off (unless we're on the last one)
      bitWrite(pattern, j--, neg);
    }
    if (i != 8)
    {
      // turn the current LED on (unless past the first one)
      bitWrite(pattern, j, pos);
    }
    
    displayPattern();
    
    // Don't delay after the last display, for more fluid transitions
    if (i != 8)
    {
      delay(delayCount);
    }
  }
}

// Michael, there's a man with an automatic weapon hiding in the bushes...
void knightRider() {
  ascendOnce();
  descendOnce();
}

// just a little different than knightRider, no pause at the ends
void pingPong() {
  ascendOnce();

  // start with the last LED
  int j = 6;
  
  // loop through all 4 LEDs (+1)
  for (int i=1; i<=7; i++)
  {
    if (i != 1)
    {
      // turn the previous LED off (unless we're on the last one)
      bitWrite(pattern, j--, neg);
    }
    if (i != 7)
    {
      // turn the current LED on (unless past the first one)
      bitWrite(pattern, j, pos);
    }
    
    displayPattern();
    
    // Don't delay after the last display, for more fluid transitions
    if (i != 7)
    {
      delay(delayCount);
    }
  }
}

// turn all on in sequence, then all off in sequence
void wipeUnwipe() {
  setPos(neg);
  ascendOnce();
  
  setPos(neg);
  ascendOnce();
}

// turn all on in reverse sequence, then blah blah blah
void epiwnUepiw() {
  setPos(neg);
  descendOnce();
  
  setPos(neg);
  descendOnce();
}

// wipe on, wipe off, Daniel San
void wipePong() {
  wipeUnwipe();
  epiwnUepiw();
}

// flash all LEDs
void quadraBlink() {
  setPos(neg);
  reset();
  delay(delayCount);
  
  setPos(neg);
  reset();
  delay(delayCount);
}

// shifts every other LED on and off
void eitherOr() {
  // getting lazy about generating patterns algorithmically
  // so just setting the nybbles by hand
  pattern = posNegPattern(0b10101010);
  displayPattern();
  delay(delayCount);
  
  pattern = posNegPattern(0b01010101);
  displayPattern();
  delay(delayCount); 
}

// shifts outer 4 LEDs and middle 4 on and off
void innerOuter() {
  
  pattern = posNegPattern(0b11000011);
  displayPattern();
  delay(delayCount);
  
  pattern = posNegPattern(0b00111100);
  displayPattern();
  delay(delayCount); 
}

// two by two-y two-y
void noahsArk() {
  
  pattern = posNegPattern(0b10000000);
  displayPattern();
  delay(delayCount); 
  
  pattern = posNegPattern(0b11000000);
  displayPattern();
  delay(delayCount); 
  
  pattern = posNegPattern(0b01100000);
  displayPattern();
  delay(delayCount); 
  
  pattern = posNegPattern(0b00110000);
  displayPattern();
  delay(delayCount);
  
  pattern = posNegPattern(0b00011000);
  displayPattern();
  delay(delayCount);
  
  pattern = posNegPattern(0b00001100);
  displayPattern();
  delay(delayCount);
  
  pattern = posNegPattern(0b00000110);
  displayPattern();
  delay(delayCount);
  
  pattern = posNegPattern(0b00000011);
  displayPattern();
  delay(delayCount);
  
  pattern = posNegPattern(0b00000001);
  displayPattern();
  delay(delayCount);
}

// false alarm, back to the farm
void noahsReturn() {
  
  pattern = posNegPattern(0b00000001);
  displayPattern();
  delay(delayCount);
  
  pattern = posNegPattern(0b00000011);
  displayPattern();
  delay(delayCount);
  
  pattern = posNegPattern(0b00000110);
  displayPattern();
  delay(delayCount);
  
  pattern = posNegPattern(0b00001100);
  displayPattern();
  delay(delayCount);
  
  pattern = posNegPattern(0b00011000);
  displayPattern();
  delay(delayCount);
  
  pattern = posNegPattern(0b00110000);
  displayPattern();
  delay(delayCount);
  
  pattern = posNegPattern(0b01100000);
  displayPattern();
  delay(delayCount); 
  
  pattern = posNegPattern(0b11000000);
  displayPattern();
  delay(delayCount); 
  
  pattern = posNegPattern(0b10000000);
  displayPattern();
  delay(delayCount); 
}
