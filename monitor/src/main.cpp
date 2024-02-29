#include "SimpleCAN.h"
#include "CANHandler.h"
#include <Arduino.h>
#include <SimpleFOC.h>
#include <math.h>


#define ID 0
// The actual CAN bus class, which handles all communication.

CANHandler CANDevice(CreateCanLib(),ID);

static uint32_t start;



// funktion umwandlung von NTC zu temperatur wird weiter unten aufgerufen 



void setup() 
{
	SimpleFOCDebug::enable();
	Serial.begin(115200);
	delay(1000);
	CANDevice.Init();
	CANDevice.Can1->SetBusTermination(true);
  start=millis();


	
  for(int i=0;i<max_device_count;i++){
    for(int j=0;j<count_target_parameter;j++){
     CANDevice.target_values[i][j]=0;
    }
  }
  for(int i=0;i<max_device_count;i++){
    for(int j=0;j<count_motor_values;j++){
      CANDevice.motor_values[i][j]=0;
    }
  }
}


void loop()
{
static uint32_t LastAction=millis();
if(LastAction+5000 < millis() ){
  Serial.printf("new Cycle : %d\n",(millis()-start)/5000);
  LastAction=millis();
}
CANDevice.Can1->Loop();
}