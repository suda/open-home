/*
  Transceiver which sends commands from computer connected via USB and is able to listen for those.
  Looks for 15 bytes (ASCII representation of Tri-State code and pulse width) 
  and sends them to transmitter module connected to pin #10 or goes into listen mode when receives "L" character.
  
  More: https://github.com/appsome/open-home/wiki/Transceiver
  
  Requires rc-switch library: http://code.google.com/p/rc-switch/

  Part of Open Home https://github.com/appsome/open-home
*/

#include <RCSwitch.h>

RCSwitch mySwitch = RCSwitch();

static char* dec2binWzerofill(unsigned long Dec, unsigned int bitLength){
  static char bin[64]; 
  unsigned int i=0;

  while (Dec > 0) {
    bin[32+i++] = (Dec & 1 > 0) ? '1' : '0';
    Dec = Dec >> 1;
  }

  for (unsigned int j = 0; j< bitLength; j++) {
    if (j >= bitLength - i) {
      bin[j] = bin[ 31 + i - (j - (bitLength - i)) ];
    }else {
      bin[j] = '0';
    }
  }
  bin[bitLength] = '\0';
  
  return bin;
}

static char* bin2tristate(char* bin) {
  char returnValue[50];
  int pos = 0;
  int pos2 = 0;
  while (bin[pos]!='\0' && bin[pos+1]!='\0') {
    if (bin[pos]=='0' && bin[pos+1]=='0') {
      returnValue[pos2] = '0';
    } else if (bin[pos]=='1' && bin[pos+1]=='1') {
      returnValue[pos2] = '1';
    } else if (bin[pos]=='0' && bin[pos+1]=='1') {
      returnValue[pos2] = 'F';
    } else {
      return "not applicable";
    }
    pos = pos+2;
    pos2++;
  }
  returnValue[pos2] = '\0';
  return returnValue;
}

void setup() {
  Serial.begin(9600);
  
  // Optional set protocol (default is 1, will work for most outlets)
  mySwitch.setProtocol(1);
  
  // Optional set number of transmission repetitions.
  mySwitch.setRepeatTransmit(10);
  
  // Transmitter is connected to Arduino Pin #10  
  mySwitch.enableTransmit(10);
  
  // Receiver is connected to Arduino interrupt #0 -> http://arduino.cc/en/Reference/attachInterrupt
  mySwitch.enableReceive(0);
}

void loop() {
  char buffer[16];
  buffer[15] = '\0';
  char pulseLength[4];
  char triState[13];
  triState[12] = '\0';
  char firstCharacter;
  
  // Wait for data
  while (Serial.available() > 0) {      
      firstCharacter = Serial.read();
        
      if (firstCharacter == 'L') {
        Serial.println("Listening...");
        // ~ 5 second timeout
        int counter = 500;
        while (!mySwitch.available() && counter > 0) {
          delay(10);
          counter--;
          
          if (Serial.available() > 0) {
            char command = Serial.read();
            if (command == 'C') counter = -1;
          }
        }
        if (mySwitch.available()) {
          char* binary = dec2binWzerofill(mySwitch.getReceivedValue(), mySwitch.getReceivedBitlength());
          Serial.print("Received pulse length: ");
          Serial.print(mySwitch.getReceivedDelay());
          Serial.print(" Tri-state code: ");
          Serial.println(bin2tristate(binary));
        } else if (counter == 0){
          Serial.println("Timed out");
        } else if (counter == -1) {
          Serial.println("Canceled");
        }
      } else {
        Serial.readBytes(buffer, 14);
        
        // Shift array by one and append first byte
        for (int i = 14; i>0; i--) {
          buffer[i+1] = buffer[i];
        }
        buffer[0] = firstCharacter;
        
        // First 3 bytes are ASCII encoded pulse length
        strncpy(pulseLength, buffer, sizeof(pulseLength));
        pulseLength[3] = '\0';
        Serial.print("Sent pulse length: ");
        Serial.print(pulseLength);      
        mySwitch.setPulseLength(atoi(pulseLength));  
        
        // Rest is Tri-state code
        memcpy(triState, &buffer[3], 12);
        Serial.print(" Tri-state code: ");
        Serial.println(triState);
        mySwitch.sendTriState(triState);
      }
  }
}
