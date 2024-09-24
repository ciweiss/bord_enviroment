#include "SimpleCAN.h"
#define max_device_count 36
#define message_space 16 // dont change
#define count_target_parameter 4
#define count_motor_values 4

class CANHandler: public SimpleCANProfile
{ 
    public:

        CANHandler(SimpleCan* pCan,int _CAN_ID) : SimpleCANProfile(pCan)
        {
           ReceivedID=-1;
           CAN_ID=_CAN_ID;
           full_instruction_recived=false;
           stop=false;
           for(int i=0;i<64;i++) id_counter[i]=false;
    
        }

        void HandleCanMessage(const SimpleCanRxHeader rxHeader, const uint8_t *rxData)
        {
            ReceivedID=rxHeader.Identifier;

            if (ReceivedID>0){
                id_counter[(ReceivedID&63)-1]=true;            }
        }

    int ReceivedID,CAN_ID;
    float motor_values[max_device_count][count_motor_values],  target_values[count_target_parameter];
    bool full_instruction_recived;
    bool stop;
    bool id_counter[64];



};

