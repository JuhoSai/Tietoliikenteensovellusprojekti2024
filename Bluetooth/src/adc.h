#ifndef ADC_H_KJJ
#define ADC_H_KJJ

typedef struct Measurement
{
   uint16_t sensor_dir; 
   uint16_t sensor_x;
   uint16_t sensor_y;
   uint16_t sensor_z;
   
};

int initializeADC(void);
struct Measurement readADCValue(void);
void printDebugInfo(void);


#endif



