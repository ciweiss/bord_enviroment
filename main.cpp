#include <Arduino.h>
#include <SimpleFOC.h>
#include <math.h>
#include <string>
// put function declarations here:
int package_count;

void setup() 
{
	SimpleFOCDebug::enable();
	Serial.begin(115200);
  delay(1000);
  Serial.println("setup");
  package_count=0;
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
  float values[144];
  byte incomingBytes[9][64];
  if (Serial.available() > 0) {
    while(package_count<9){
      if (Serial.available() > 0){
        Serial.readBytes(incomingBytes[package_count],64);
        package_count++;
      }
    }
  }
  if(package_count==9){
    for(int i=0;i<9;i++){
      for(int j=0;j<16;j++){
        byte temp[4]={incomingBytes[i][j*4],incomingBytes[i][j*4+1],incomingBytes[i][j*4+2],incomingBytes[i][j*4+3]};
        values[i*16+j]=bit_conversion(temp);
      }
    }
    package_count=0;
    Serial.print("ENDE");
  }
  

}
