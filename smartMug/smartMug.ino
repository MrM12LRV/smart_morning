
#include <math.h>
#include <DallasTemperature.h>
#include <OneWire.h>
#define ONE_WIRE_BUS 3 //io pin

//CHECK PINS!!!!!!!!!!!!!!!!!!!!!!!!!!1

uint8_t greenLED = 13; //digWrite
uint8_t redLED = 12; //digWrite

float TEMP1;
float TEMP2;


// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);

void setup() {
  pinMode(greenLED, OUTPUT);
  pinMode(redLED, OUTPUT);  
  digitalWrite(greenLED,LOW);
  digitalWrite(redLED,LOW);

  
  Serial.begin(9600);
  
  sensors.begin();
  sensors.setWaitForConversion(false);

}

void loop() {
  
  sensors.requestTemperatures(); 
  TEMP1 = sensors.getTempCByIndex(0); 
  TEMP2 = sensors.getTempCByIndex(1);
  Serial.println(TEMP1); //debug
  Serial.println(TEMP2); //debug
  if (TEMP1 > 30){
    digitalWrite(greenLED,HIGH);
    delay(2000);
    digitalWrite(greenLED,LOW);
  }
  else {
    digitalWrite(redLED,HIGH);
    delay(2000);
    digitalWrite(redLED,LOW);
  }
  

  delay(500);
}
