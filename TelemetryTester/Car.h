#ifndef CAR_H
#define CAR_H

// Variables to hold raw sensor values with full precision
struct Car_Raw {
	uint16_t RPM;
	int16_t Torque;
	uint16_t RPM_Front_Left;
	uint16_t RPM_Front_Right;
	uint16_t RPM_Rear_Left;
	uint16_t RPM_Rear_Right;
	uint16_t Temp_IGBT;
	uint16_t Temp_Motor;
	uint16_t Temp_BrakeLeft;
	uint16_t Temp_BrakeRight;
	uint16_t Throttle_12;
	uint16_t Throttle_5;
	uint16_t Brake_Front;
	uint16_t Brake_Rear;
	int32_t Current_IVT;
	uint32_t Voltage_IVT;
	uint8_t VCU_ETD;
	uint8_t VCU_BMSA;
	uint8_t VCU_MCMS;
	uint8_t VCU_CPS;
	uint16_t VCU_EMA;
	uint16_t VCU_PLS;
	uint16_t Temp_Coolant_In;
	uint16_t Temp_Gearbox;
	uint16_t Temp_Coolant_Out;
	uint16_t Voltage_BMS_Min_Left;
	uint16_t Voltage_BMS_Min_Right;
	uint16_t Voltage_BMS_Max_Left;
	uint16_t Voltage_BMS_Max_Right;
	uint16_t Temp_BMS_Min_Left;
	uint16_t Temp_BMS_Max_Left;
	uint16_t Temp_BMS_Min_Right;
	uint16_t Temp_BMS_Max_Right;
	uint16_t Current_Low_Battery;
};

// Variables to hold normalized sensor values with full precision
struct Car_Processed {
	uint16_t RPM;
	int16_t Torque; // TODO: Unit? Range?
	uint16_t RPM_Front_Left;
	uint16_t RPM_Front_Right;
	uint16_t RPM_Rear_Left;
	uint16_t RPM_Rear_Right;
	float Temp_IGBT;
	float Temp_Motor;
	float Temp_BrakeLeft;
	float Temp_BrakeRight;
	uint8_t Throttle; // %
	uint8_t Brake_Front; // Bar 0-200
	uint8_t Brake_Rear; // Bar 0-200
	float Current_IVT; // TODO: Unit?
	float Voltage_IVT;
	uint8_t VCU_ETD;
	uint8_t VCU_BMSA;
	uint8_t VCU_MCMS;
	uint8_t VCU_CPS;
	uint16_t VCU_EMA;
	uint16_t VCU_PLS;
	float Temp_Coolant_In;
	float Temp_Gearbox;
	float Temp_Coolant_Out;
	float Voltage_BMS_Min_Left;
	float Voltage_BMS_Min_Right;
	float Voltage_BMS_Max_Left;
	float Voltage_BMS_Max_Right;
	float Temp_BMS_Min_Left;
	float Temp_BMS_Max_Left;
	float Temp_BMS_Min_Right;
	float Temp_BMS_Max_Right;
	float Current_Low_Battery; // TODO: Amps? Unit?
};

struct Car_Mixed {
	Car_Raw Raw; // Don't use for the tests
	Car_Processed Processed;
	uint8_t datapack_left_box[96];
	uint8_t datapack_right_box[96];
};

Car_Mixed Car;

#endif