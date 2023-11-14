#include <Arduino.h>
#include <SimpleFOC.h>
#include <math.h>
#include <string>
// put function declarations here:


void setup() 
{
	SimpleFOCDebug::enable();
	Serial.begin(115200);
	delay(1000);
  Serial.println("setup");

}

float bit_conversion(byte bits[4]){
  float f=0;
  uint8_t tmp[4];
  for (size_t j = 0; j < 4; j++) {
    tmp[j] = bits[j];
  }
  memcpy(&f, &tmp, 4);
  return f;
}
void loop() {
  delay(1000);
  float temp=0;
  byte controll[4];
  byte incomingByte[4];
   if (Serial.available() > 0) {
    delay(10000);
    Serial.readBytes(incomingByte,4);
    
    temp=bit_conversion(incomingByte);
    Serial.print(temp,8);
    Serial.print("\n");
    Serial.print("Bytes:\n");
    for(size_t i=0;i<4;i++){
      Serial.print(incomingByte[i]);
      Serial.print("\n");
    }
    memcpy(&controll, &temp, 4);
        for(size_t i=0;i<4;i++){
      Serial.print(controll[i]);
      Serial.print("\n");
    }
    Serial.print("\n");
  }

}

// put function definitions here:
