/*
  Basic serial bridge between computer and transmitter.
  Looks for 15 bytes (ASCII representation of Tri-State code and pulse width) 
  and sends them to transmitter.
  
  More: https://github.com/appsome/open-home/wiki/Bridge
  
  Requires rc-switch library: http://code.google.com/p/rc-switch/

  Part of Open Home https://github.com/appsome/open-home
*/

#include <RCSwitch.h>

RCSwitch mySwitch = RCSwitch();

void setup() {
  Serial.begin(9600);
  
  // Optional set protocol (default is 1, will work for most outlets)
  mySwitch.setProtocol(1);
  
  // Optional set number of transmission repetitions.
  mySwitch.setRepeatTransmit(10);
  
  // Transmitter is connected to Arduino Pin #10  
  mySwitch.enableTransmit(10);
}

void loop() {
  char buffer[16];
  buffer[15] = '\0';
  char pulseLength[4];
  char triState[13];
  triState[12] = '\0';
  
  // Wait for 15 bytes on serial
  while (Serial.available() > 0) {      
      Serial.readBytes(buffer, 15);

      // First 3 bytes are ASCII encoded pulse length
      strncpy(pulseLength, buffer, sizeof(pulseLength));
      pulseLength[3] = '\0';
      Serial.print("Pulse length: ");
      Serial.print(pulseLength);      
      mySwitch.setPulseLength(atoi(pulseLength));  
      
      // Rest is Tri-state code
      memcpy(triState, &buffer[3], 12);
      Serial.print(" Tri-state code: ");
      Serial.println(triState);
      mySwitch.sendTriState(triState);
  }
}
