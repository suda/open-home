/*
  Basic serial bridge between computer and transmitter.
  Version fot Arduino Yun.
  
  Requires rc-switch library: http://code.google.com/p/rc-switch/

  Part of Open Home https://github.com/appsome/open-home
*/

#include <RCSwitch.h>
#include <Bridge.h>
#include <YunServer.h>
#include <YunClient.h>

// Transmitter is connected to ATTiny Pin #2
#define TRANSMIT_PIN 2

RCSwitch mySwitch = RCSwitch();
YunServer server;

void setup() {
  // Optional set protocol (default is 1, will work for most outlets)
  mySwitch.setProtocol(1);
  
  // Optional set number of transmission repetitions.
  mySwitch.setRepeatTransmit(10);
  
  pinMode(TRANSMIT_PIN, OUTPUT);  
  mySwitch.enableTransmit(TRANSMIT_PIN);
  
  // Initiate Yun bridge
  Bridge.begin();
  
  // Start web server
  server.listenOnLocalhost();
  server.begin();
}

void loop() {
  YunClient client = server.accept();

  if (client) {
    process(client);
    client.stop();
  }

  delay(50);
  
  char buffer[16];
  buffer[15] = '\0';
  char pulseLength[4];
  char triState[13];
  triState[12] = '\0';
  
  int i = 0;
  // Wait for 15 bytes on serial
//  while (mySerial.available() > 0) {
//      while (i < 15) {
//        buffer[i] = mySerial.read();
//        i++;
//      }    
//      i = 0;
//      
//      // First 3 bytes are ASCII encoded pulse length
//      strncpy(pulseLength, buffer, sizeof(pulseLength));
//      pulseLength[3] = '\0';
//      mySerial.print("Pulse length: ");
//      mySerial.print(pulseLength);
//      mySwitch.setPulseLength(atoi(pulseLength));  
//      
//      // Rest is Tri-state code
//      memcpy(triState, &buffer[3], 12);
//      mySerial.print(" Tri-state code: ");
//      mySerial.println(triState);
//      mySwitch.sendTriState(triState);
//  }
}

void process(YunClient client) {
  String command = client.readStringUntil('/');

  if (command == "433") {
    parse433(client);
  }
}

void parse433(YunClient client) {
  int pulseLength;
  String triStateString;
  char triStateCode[13];
  triStateCode[12] = '\0';
  
  pulseLength = client.parseInt();
  mySwitch.setPulseLength(pulseLength);
  
  if (client.read() == '/') {
    triStateString = client.readStringUntil('/');
    triStateString.toCharArray(triStateCode, 12);
    mySwitch.sendTriState(triStateCode);
    client.print(F("Sent "));
    client.println(triStateString);
  } else {
    client.print(F("Unsufficient paramenters"));  
  }
}
