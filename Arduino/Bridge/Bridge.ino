/*
  Basic serial bridge between computer and transmitter.
  Looks for 12 bytes (ASCII representation of Tri-State code) and sends them to transmitter.
  
  Requires rc-switch library: http://code.google.com/p/rc-switch/

  Part of Open Home https://github.com/appsome/open-home
*/

#include <RCSwitch.h>

RCSwitch mySwitch = RCSwitch();

void setup() {
  Serial.begin(9600);
  
  // Optional set protocol (default is 1, will work for most outlets)
  mySwitch.setProtocol(1);

  // Set pulse length.
  mySwitch.setPulseLength(232);
  
  // Optional set number of transmission repetitions.
  mySwitch.setRepeatTransmit(10);
  
  // Transmitter is connected to Arduino Pin #10  
  mySwitch.enableTransmit(10);
}

void loop() {
  char buffer[13];
  buffer[12] = '\0';
  
  // Wait for 12 bytes on serial
  while (Serial.available() > 0) {      
      Serial.readBytes(buffer, 12);
      // Echo
      Serial.println(buffer);
      // Send thru RF
      mySwitch.sendTriState(buffer);
  }
}
