/*
  Basic webserver and transmitter. 
  Version for Arduino Yun.
  
  More: https://github.com/appsome/open-home/wiki/TransmitterYun  
  
  Requires rc-switch library: http://code.google.com/p/rc-switch/

  Part of Open Home https://github.com/appsome/open-home
*/

#include <RCSwitch.h>
#include <Bridge.h>
#include <YunServer.h>
#include <YunClient.h>

// Transmitter is connected to Arduino Pin #9
#define TRANSMIT_PIN 9

// WARNING: Set to your own values from https://github.com/appsome/open-home/wiki/Recording-codes
#define ON_PULSE_LENGTH "209"
#define ON_TRISTATE "FF000FFF0101"
#define OFF_PULSE_LENGTH "209"
#define OFF_TRISTATE "FF000FFF0110"

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
}

void process(YunClient client) {
  String command = client.readStringUntil('/');

  if (command == "433") {
    parse433(client);
  } else {
    responseIndex(client);
  }
}

void parse433(YunClient client) {
  int pulseLength;
  String triStateString;
  char triStateCode[13];
  
  pulseLength = client.parseInt();
  mySwitch.setPulseLength(pulseLength);
  
  if (client.read() == '/') {
    triStateString = client.readStringUntil('/');
    triStateString.toCharArray(triStateCode, 13);
    mySwitch.sendTriState(triStateCode);

    client.println(F("Status: 301"));
    client.println(F("Location: /arduino/index.html"));
    client.println();
    client.print(F("{ \"sent\": \""));
    client.print(triStateCode);
    client.print(F("\" }"));
  } else {
    client.print(F("{ \"error\": \"Unsufficient paramenters\" }"));  
  }
}

void responseIndex(YunClient client) {
  client.println(F("Status: 200"));
  client.println(F("Content-type: text/html"));
  client.println();
  
  client.print(F("<a href=\"/arduino/433/"));
  client.print(ON_PULSE_LENGTH);
  client.print(F("/"));
  client.print(ON_TRISTATE);
  client.print(F("\">ON</a><br>"));
  
  client.print(F("<a href=\"/arduino/433/"));
  client.print(OFF_PULSE_LENGTH);
  client.print(F("/"));
  client.print(OFF_TRISTATE);
  client.print(F("\">OFF</a><br>"));
}
