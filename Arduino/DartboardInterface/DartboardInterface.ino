/*
  Dartboard Interface
  
      Copyright (C) 2013  Tim Kracht <timkracht4@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
    
  Reads the dartboard as a 10x7 matrix of buttons.
  
  Sends pulses from arduino to one axis of the matrix
  through two daisy chained 74HC595 serial-to-parallel
  shift registers.
  
  Reads from the other axis through a single 74HC589
  parallel-to-serial shift register.
*/

#include "pitches.h"


//////////////////////////////////////////////////////////////
//  Defines
//////////////////////////////////////////////////////////////

// Pin connected to latch pin (ST_CP) of 74HC595
#define LATCH_SIPO     5
// Pin connected to clock pin (SH_CP) of 74HC595
#define CLOCK_SIPO     6
// Pin connected to Data in (DS) of 74HC595
#define DATA_SIPO      7

// Pin connected to serial-shift/ parallel-load pin of 74HC589
#define SS_PL_PISO    11
// Pin connected to latch clock pin of 74HC589
#define LATCH_PISO    10
// Pin connected to shift clock pin of 74HC589
#define CLOCK_PISO     9
// Pin connected to Data out (QW/QH?) of 74HC589
#define DATA_PISO      8

// Pin connected to speaker
#define SPEAKER_PORT  12

// set this to false if you don't have a speaker hooked up to digit pin 12 
#define HAS_SPEAKER true

// the column/pin on the board wired to the bulls-eye
// for special handling
#define BULL_BOARD_COLUMN_PIN   3

// Interface commands
#define IFACE_HIT           'H'
#define IFACE_CONNECT       'C'
#define IFACE_DISCONNECT    'D'
#define IFACE_PLAY          'P'
#define IFACE_STOP          'X'
#define IFACE_QUERY_STATE   'Q'

//////////////////////////////////////////////////////////////
//  Variable Declarations
//////////////////////////////////////////////////////////////


// data to send to shift register for each board row/pin
byte shiftRows1[10] = {64,128,0,0,0,0,0,0,0,0};
byte shiftRows2[10] = {0,0,1,2,4,8,16,32,64,128};

// the segment multipliers
byte multipliers[4] = {0,1,2,3};

// The wedges wired to rows/pins 0-9 of board
// The third value is special case for bulls-eye multiplier
byte boardWedges[10][3] = {  {1,7,0}, 
                            {18,19,0}, 
                            {4,3,0}, 
                            {13,17,0}, 
                            {6,2,0}, 
                            {10,15,0}, 
                            {20,16,0}, 
                            {5,8,0}, 
                            {12,11,1}, 
                            {9,14,2}    };

    
// The rings wired to columns/pins 1-7 of board.
// The first value is which half of the board was hit
//   and is used to pick the correct boardWedge value from the
//   boardWedges array.
// The second value is the multiplier ring that was hit, 1=single,
//   2=double, 3=triple
// Bulls-eye is special case where the value is determined here,
//   and mulitplier is handled in the boardWedges array.
byte boardRings[7][2] = {  {0,3},
                          {0,2},
                          {0,1},
                          {2,25},
                          {1,1},
                          {1,2},
                          {1,3}    };

char gameState;

int rowHit = -1;
int columnHit = -1;

//////////////////////////////////////////////////////////////
//  Main
//////////////////////////////////////////////////////////////

// the setup routine runs once when you press reset:
void setup() {     
  Serial.begin(9600);
  
  //set pins to output to control the 74HC595
  pinMode(LATCH_SIPO, OUTPUT);
  pinMode(CLOCK_SIPO, OUTPUT);
  
  // set pin to output to write serial data to 74HC595
  pinMode(DATA_SIPO, OUTPUT);
  
  //set pins to output to control the 74HC589
  pinMode(SS_PL_PISO, OUTPUT);
  pinMode(LATCH_PISO, OUTPUT);
  pinMode(CLOCK_PISO, OUTPUT);
  
  // set pin to input to read serial data from 74HC589
  pinMode(DATA_PISO, INPUT);
  
  // set latch pin IN to low and load pin to high initially
  digitalWrite(LATCH_PISO, LOW);
  digitalWrite(SS_PL_PISO, HIGH);
  
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }
  
  gameState = IFACE_DISCONNECT;
}

// the loop routine runs over and over again forever and ever and ever:
void loop() {
  if (gameState == IFACE_PLAY) {
    // check for a hit
    for (int row=0; row < 10; row++) {
       setSipoRow(row);
       processPisoColumns(row);
    }
  }
  else {
    delay(1000);
  }
}

// automatically called between loops when serial data is available
void serialEvent() {
    switch (Serial.read()) {
      case IFACE_QUERY_STATE:
        Serial.print(gameState);
        break;
      case IFACE_CONNECT:
        if (gameState == IFACE_DISCONNECT) {
          gameState = IFACE_STOP;
          Serial.write(IFACE_CONNECT);
        }
        break;
      case IFACE_DISCONNECT:
        if (gameState != IFACE_DISCONNECT) {
          gameState = IFACE_DISCONNECT;
          Serial.write(IFACE_DISCONNECT);
        }
        break;
      case IFACE_PLAY:
        if (gameState == IFACE_STOP) {
          gameState = IFACE_PLAY;
          Serial.write(IFACE_PLAY);
          playCharge();
        }
        break;
      case IFACE_STOP:
        if (gameState == IFACE_PLAY) {
          gameState = IFACE_STOP;
          Serial.write(IFACE_STOP);
        }
        break;
      default:
        break;  
    }
}


//////////////////////////////////////////////////////////////
//  Helpers
//////////////////////////////////////////////////////////////


// sets the SIPO shift register to power the correct row
void setSipoRow(int rowNumber) {
      // take the shift out latchPin low to shift it out
      digitalWrite(LATCH_SIPO, LOW);
      
      // shift out the bits:
      shiftOut(DATA_SIPO, CLOCK_SIPO, MSBFIRST, shiftRows1[rowNumber]);
      shiftOut(DATA_SIPO, CLOCK_SIPO, MSBFIRST, shiftRows2[rowNumber]);
      
      //take the shift out latch pin high so the voltage is sent
      // to the next row (or none if looking at the first 2 rows):
      digitalWrite(LATCH_SIPO, HIGH);
}

// check each column in the given row for a hit
void processPisoColumns(int row) {
      
      loadPisoColumns();
       
      // check each column of the PISO for a hit
      for (int column = 0; column < 8; column++)
      {        
        if (digitalRead(DATA_PISO) == HIGH)
        {          
          // set the hit coords to watch for the unpressing
          rowHit = row;
          columnHit = column;
        }
        else if (row == rowHit && column == columnHit)
        {
          // button has been unpressed, register the hit
          rowHit = -1;
          columnHit = -1;
          registerHit(row,column);
        }
        
        // shift
        digitalWrite(CLOCK_PISO, HIGH);
        digitalWrite(CLOCK_PISO, LOW);
      }
}

// loads the parallel input values into the PISO shift register
void loadPisoColumns() {
      
      // move PISO latch from LOW to HIGH to move parallel inputs to data latch
      digitalWrite(LATCH_PISO, HIGH);
      
      // reset the PISO latch
      digitalWrite(LATCH_PISO, LOW);
      
      // move the PISO SS-PL pin from high to low load the data from the data latch 
      // to the shift registers
      digitalWrite(SS_PL_PISO, LOW);
  
      // move PISO SS-PL pin from low to high to enable shifting
      digitalWrite(SS_PL_PISO, HIGH);
}

// does whatever needs to be done when a wedge is hit by a dart
// like send a message out to the serial port
void registerHit(int row, int column) {
  
  byte multiplierCode;
  byte wedgeValue;
  
  // bulls-eye is opposite the rest: the wedge is wired to the columns 
  // and the multipliers are wired to the rows
  if (column == BULL_BOARD_COLUMN_PIN) {
    // confusing, write it all out and it might make sense
    multiplierCode = multipliers[boardWedges[row][boardRings[column][0]]];
    wedgeValue = boardRings[column][1];
  }
  else {
    // still confusing, write it all out and it might not make sense
    multiplierCode = multipliers[boardRings[column][1]];
    wedgeValue = boardWedges[row][boardRings[column][0]];
  }
  
  Serial.write(IFACE_HIT);
  Serial.write(wedgeValue);
  Serial.write(multiplierCode);
}

void playCharge() {
  int notes[] = {NOTE_G3, NOTE_C4, NOTE_E4, NOTE_G4, NOTE_E4, NOTE_G4};
  int durations[] = {8, 8, 8, 4, 8, 2};
  int noteCount = 6;
  
  playMelody(notes, durations, noteCount);
}

// based on the arduino tones example, plays the given melody
void playMelody(int melody[], int noteDurations[], int notecount) {
  // don't even try to play nothin' if we don't got no speaker
  if (HAS_SPEAKER) {
    noTone(SPEAKER_PORT);
    
    // iterate over the notes of the melody:
    for (int thisNote = 0; thisNote < notecount; thisNote++) {
  
      // to calculate the note duration, take one second 
      // divided by the note type.
      //e.g. quarter note = 1000 / 4, eighth note = 1000/8, etc.
      int noteDuration = 1000/noteDurations[thisNote];
      tone(SPEAKER_PORT, melody[thisNote], noteDuration);
  
      // to distinguish the notes, set a minimum time between them.
      // the note's duration + 30% seems to work well:
      int pauseBetweenNotes = noteDuration * 1.30;
      delay(pauseBetweenNotes);
      
      // stop the tone playing:
      noTone(SPEAKER_PORT);
    }
  }
}
