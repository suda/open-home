/*
  Basic serial bridge between computer and transmitter.
  Version fot ATTiny 45/85 microcontrollers.
  Looks for 15 bytes (ASCII representation of Tri-State code and pulse length)
  and sends them to transmitter.
  
  Requires rc-switch library: http://code.google.com/p/rc-switch/

  Part of Open Home https://github.com/appsome/open-home
*/

#include <RCSwitch.h>
#include <SoftwareSerial.h>

RCSwitch mySwitch = RCSwitch();
SoftwareSerial mySerial(4, 3);

void setup() {
  // Base value got from TinyTuner, but had to adjust manually
  OSCCAL = 0x83;
  
  mySerial.begin(9600);
  
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
  
  int i = 0;
  // Wait for 15 bytes on serial
  while (mySerial.available() > 0) {
      while (i < 15) {
        buffer[i] = mySerial.read();
        i++;
      }    
      i = 0;
      
      // First 3 bytes are ASCII encoded pulse length
      strncpy(pulseLength, buffer, sizeof(pulseLength));
      pulseLength[3] = '\0';
      mySerial.print("Pulse length: ");
      mySerial.print(pulseLength);
      mySwitch.setPulseLength(atoi(pulseLength));  
      
      // Rest is Tri-state code
      memcpy(triState, &buffer[3], 12);
      mySerial.print(" Tri-state code: ");
      mySerial.println(triState);
      mySwitch.sendTriState(triState);
  }
}
