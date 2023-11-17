#include <Arduino.h>

#define max_device_count 36
#define message_space 16
#define count_target_parameter 4// must be multiple of 4
#define count_motor_values 4    // must be multiple of 4

float target_values[max_device_count][count_target_parameter];
byte ByteBuffer[9][64];
void setup() 
{
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
void send_values_serial(){
  for(int i=0;i<9;i++){
    Serial.write(ByteBuffer[i],64);
  }
}
void can_to_bytes(){
  byte temp[4];
  int value_count=0;
  for(int i=0;i<9;i++){
    for(int j=0;j<16;j++){
      memcpy(&temp,&target_values[value_count/4][value_count%4],4);
      ByteBuffer[i][j*4]  =temp[0];
      ByteBuffer[i][j*4+1]=temp[1];
      ByteBuffer[i][j*4+2]=temp[2];
      ByteBuffer[i][j*4+3]=temp[3];
      value_count++;
    }
  }
}
void flush_buffer(){
  for(int i=0;i<9;i++){
    for(int j=0;j<64;j++){
      ByteBuffer[i][j]=0;
    }
  }
}
void get_values_serial(){
  if (Serial.available() > 0) {
    int package_count=0;
    while(package_count<9){
      if (Serial.available() > 0){
        Serial.readBytes(ByteBuffer[package_count],64);
        Serial.write(package_count);
        package_count++;
      }
    }
    int value_counter=0;
    for(int i=0;i<9;i++){
      for(int j=0;j<16;j++){
        byte temp[4]={ByteBuffer[i][j*4],ByteBuffer[i][j*4+1],ByteBuffer[i][j*4+2],ByteBuffer[i][j*4+3]};
        target_values[value_counter/4][value_counter%4]=bit_conversion(temp);
        value_counter++;
      }
    }
    package_count=0;
    delay(10000);
    flush_buffer();
    can_to_bytes();
    send_values_serial();
  }
}


void loop() {
  get_values_serial();

}
