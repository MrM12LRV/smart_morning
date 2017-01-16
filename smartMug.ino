
#include <math.h>
#include <DallasTemperature.h>
#include <OneWire.h>


//CHECK PINS!!!!!!!!!!!!!!!!!!!!!!!!!!1

greenLED = 4; //digWrite
redLED = 3; //digWrite
#define ONE_WIRE_BUS 3 //io pin
//#define ONE_WIRE_BUS 2
//#define ONE_WIRE_PWR 3
//#define ONE_WIRE_GND 4

// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);

void setup() {
  pinmode(greenLED, OUTPUT);
  pinmode(redLED, OUTPUT);  
  digitalWrite.greenLED(LOW);
  digitalWrite.redLED(LOW);

  
  Serial.begin(9600);
  
  sensors.begin();
  sensors.setResolution(tempSensor, 12);
  sensors.setWaitForConversion(false);

}

void loop() {
  sensors.requestTemperatures(); 
  TEMP1 = sensors.getTempCByIndex(0); 
  TEMP2 = sensors.getTempCByIndex(1);
  Serial.println(TEMP1); //debug
  Serial.println(TEMP2); //debug
  //digitalWrite.greenLED(HIGH);
  //delay(2000);
  //digitialWrite.greenLED(LOW);

  //delay again?

}
