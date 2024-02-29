#include "SimpleCAN.h"
#define max_device_count 36
#define message_space 16
#define count_target_parameter 4
#define count_motor_values 4

class CANHandler: public SimpleCANProfile
{ 
    public:

        CANHandler(SimpleCan* pCan,int _CAN_ID) : SimpleCANProfile(pCan)
        {
           Value=0;
           ReceivedID=-1;
           CAN_ID=_CAN_ID;
           full_instruction_recived=false;

        }
        int IDHandler(int i){
	       if(CAN_ID==0){
		        if(((i/message_space)>0)&&((i%message_space)>=message_space/2)){
			        return (i%message_space)-(message_space/2);
		        }
	        }else{
		        if(CAN_ID==(i/message_space)&& (i%message_space)<(message_space/2)){
			        return i%message_space;
		        }
	        }
	        return -1;
        }

        void HandleCanMessage(const SimpleCanRxHeader rxHeader, const uint8_t *rxData)
        {
            Value=CANGetFloat(rxData);
            ReceivedID=rxHeader.Identifier;
            if (ReceivedID!=-1){
                        Serial.printf("Recived message withID:%d , value:%f\n",ReceivedID,Value);
	            
            }
        }
        void get_target_values(){
            while(!full_instruction_recived){
                Can1->Loop();
            }
        }
        void send_target_values(){
            for(int i=1;i<max_device_count;i++){
				for(int j=0;j<count_target_parameter;j++){
                    CANSendFloat(target_values[i][j],i*message_space+j);
     		        delay(10);
                    //Serial.printf("Send id:%d with value:%f\n",i*message_space+j,target_values[i][j]);
                }
            }
        }
        void send_motor_values(){
			for(int j=0;j<count_motor_values;j++){
                CANSendFloat(motor_values[CAN_ID][j],CAN_ID*message_space+j+(message_space/2));
     		    Serial.printf("Send id:%d with value:%f\n",CAN_ID*message_space+j+(message_space/2),motor_values[CAN_ID][j]);
            }
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
                memcpy(&temp,&motor_values[value_count/4][value_count%4],4);
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
        bool get_values_serial(){
            if (Serial.available() > 0) {
                int package_count=0;
                while(package_count<9){
                    if (Serial.available() > 0){
                        Serial.readBytes(ByteBuffer[package_count],64);
                        package_count++;
                        Serial.write(package_count);
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
                can_to_bytes();
                send_values_serial();
                return true;
            }
            return false;
      
        }
    int ReceivedID,CAN_ID;
    float Value, motor_values[max_device_count][count_motor_values],target_values[max_device_count][count_target_parameter];
    bool full_instruction_recived;
    byte ByteBuffer[9][64];



};

