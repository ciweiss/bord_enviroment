#include "SimpleCAN.h"
#include "CANHandler.h"
#include <Arduino.h>
#include <SimpleFOC.h>
#include <math.h>


#define ID 16
CANHandler CANDevice(CreateCanLib(),ID);


uint8_t testload[16];







static float Ntc2TempV(float ADCVoltage) 
{
	// Formula: https://www.giangrandi.org/electronics/ntc/ntc.shtml
	const float ResistorBalance = 4700.0;
	const float Beta  = 3425.0F;
	const float RoomTempI = 1.0F/298.15F; //[K]
	const float Rt = ResistorBalance * ((3.3F / ADCVoltage)-1);
	const float R25 = 10000.0F;
	
	float T = 1.0F/((log(Rt/R25)/Beta)+RoomTempI);
	T = T - 273.15;

	return T;
}


void setup() 
{
	SimpleFOCDebug::enable();
	Serial.begin(115200);
	delay(1000);
  Serial.println("setup");
  Serial.println("Firmware 2.1");
  Serial.printf("Id: %d\n",ID);
  CANDevice.Init();
	CANDevice.Can1->SetBusTermination(true);
  if(ID>0){
    FilterDefinition FilterConfig2;
    FilterConfig2.IdType = CAN_STDID;
    FilterConfig2.FilterIndex = 0;
    FilterConfig2.FilterType = CAN_FILTER_MASK;
    FilterConfig2.FilterConfig = CAN_FILTER_TO_RXFIFO0;
    FilterConfig2.FilterID1 = 0;
    FilterConfig2.FilterID2 = 0;
    CANDevice.Can1->ConfigFilter(&FilterConfig2);
  }

  float test=16;
  for(int i=0;i<16;i++){
    testload[i]=i+1;
  }
  memcpy(testload,&test,4);

}


void loop()
{

  static uint32_t LastAction=millis();
  static uint32_t LastAction2=millis();
  CANDevice.Can1->TriggerSending();

  if (LastAction+5000<millis()){
    CANDevice.Can1->SendMessage(testload,16,0);
    CANDevice.Can1->SendMessage(testload,16,64);
    LastAction=millis();
  }
  if (LastAction2+15000<millis()){
    Serial.printf("Not found:\n");
    for(int i=1;i<37;i++){
      if(!CANDevice.id_counter[i-1]) Serial.printf("ID: %d\n",i);
      CANDevice.id_counter[i-1]=false;
    }
    LastAction2=millis();
  }
  CANDevice.Can1->Loop();
}