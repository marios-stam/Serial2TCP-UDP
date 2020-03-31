#ifndef TELEMETRYPACKET_H
#define TELEMETRYPACKET_H

/* Transmission Protocol

    The transmitted data are structured in this described manner:
        Settings:
            Indicates which packets are transmitted (order matters)
        Timestamp:
            Index and system time in ms before transmission (queueing)
        Payload:
            All the packets selected by the settings in specific order

    The data are queued by the Transmit() function and transmitted when the device is available.
    This prevents blocking while calling the Transmit() function.
    Each packet is queued and removed once successfully transmitted.
    The queue uses a circular ring buffer to ensure minimum packet losses.

*/

/* Transmission Settings Packet 
    The purpose of the telemetry software implemented in this project is to monitor the
    performance and safety of the car, in near real-time, while it is racing. While the
    car has a lot of useful sensors installed, we don't need to send all of them to the
    telemetry GUI continuously. So we need a way to select which sensors we want to view.
    To achieve that, when we send the start packet from the GUI to the car, to initiate
    the telemetry, we specify the SelectiveSampling variable. The SelectiveSampling selects 
    which packets to include in the transmission
        MSB:    Not used yet. Soon to be used for precision.
        Bit 6:  Performance
        Bit 5:  BMS 
        Bit 4:  Temperatures
        Bit 3:  Pedals
        Bit 2:  Wheels
        Bit 1:  VCU
        LSB:    IMU
    This way we only enable the transmission of the needed information and save bandwidth.
    This can be modified from the GUI at any time, even when the telemetry is running.
    To save more bandwidth, the information sent from the car to the GUI are not stamped.
    This means that we don't explicitly declare what each byte represents in the packet.
    To overcome this we have to use a fixed positioning system for the bytes in the packet.
    This is done by having a specific order of the information laid in the telemetry packet.
    Although we still need to know what information is included in the packet. To solve this
    we include the SelectiveSampling variable in the transmitted packet so the GUI can now 
    interpret the received bytes to their corresponding variables. For example if the 
    SelectiveSampling = 85 = (0101 0101) then we know that after the timestamp bytes the
    first sizeof(Packet_Performance) bytes are for the performance information. Then the next
    sizeof(Temperatures) bytes are for the temperatures etc. 
*/
const uint8_t MASK_PERF   = B01000000;
const uint8_t MASK_BMS    = B00100000;
const uint8_t MASK_TEMP   = B00010000;
const uint8_t MASK_PEDALS = B00001000;
const uint8_t MASK_WHEELS = B00000100;
const uint8_t MASK_VCU    = B00000010;
const uint8_t MASK_IMU    = B00000001;
const uint8_t SELECTIVE_SAMPLING_DEFAULT = B01111110;
// TODO: Load from EEPROM
uint8_t Telemetry_SelectiveSampling = SELECTIVE_SAMPLING_DEFAULT;
struct Packet_Settings {
    uint8_t SelectiveSampling;
};

/* Timestamp Packet
    The purpose of the telemetry software implemented in this project is to monitor the
    performance and safety of the car, in near real-time, while it is racing. Due to
    losses and delays caused by processing or transmitting the data over the air, we need
    to implement a synchronized communication protocol. To achieve that, each packet 
    transmitted from the car needs to be uniquely identified and marked with the time details
    needed to correctly process and display it at the telemetry GUI. Because the bandwidth is 
    limited we need to compress those information to minimize the overhead of each packet.
    Based on the fact that the low voltage system of the car, thus the telemetry software too,
    won't be active for more than 6 hours continuously, we can utilize 3 bytes for storing the
    index and timestamp of each packet. Of course the Teensy platform doesn't provide 24bit
    variables we need to create our own datatype. For making the code more readable I decided
    to split the 3 byte variable into 3 descrete bytes. This will also help the processing of
    the received packet at the GUI.
    Naming convention:
        MSB = Most significant byte
        MMSB = Middle most significant byte
        LSB = Least significant byte
    Index:
        The 3 byte variable can hold 16777216 (2^24) descrete indices which, at 100Hz 
        transmission frequency, can identify packets for more than 46 hours continuously.
    Timestamp:
        The Teensy platform uses unsigned long for the millis() implementation which is a
        4 byte variable type. With the 3 byte custom variable the telemetry software can 
        handle timestamps for up to 4.6 hours
    The overflow of the variables need to be addressed and is crucial.
*/
struct Packet_Timestamp {
    uint8_t IndexMSB;
    uint8_t IndexMMSB;
    uint8_t IndexLSB;
    uint8_t TimestampMSB;
    uint8_t TimestampMMSB;
    uint8_t TimestampLSB;
};

/* Performance Packet
    Not compressed
*/
struct Packet_Performance {
    uint16_t RPM;
    int16_t Torque;
    int16_t IVT_Current;
    uint16_t IVT_Voltage;
};

/* BMS Packet
    Voltages:
        Bias: 1.7 V
        Range: 1.7-4.25 V
        Precision: 0.01 V
        CompressedValue = (uint8_t)floor((RawValue - 1.7) * 100);
    Temperatures:
        Bias: 0
        Range: 0-128 C
        Precision: 0.5 C
        CompressedValue = (uint8_t)floor(RawValue * 2);
*/
struct Packet_BMS {
    byte Faults;
    uint8_t Voltage_Min_Left;
    uint8_t Voltage_Min_Right;
    uint8_t Voltage_Max_Left;
    uint8_t Voltage_Max_Right;
    uint8_t Temp_Min_Left;
    uint8_t Temp_Max_Left;
    uint8_t Temp_Min_Right;
    uint8_t Temp_Max_Right;
};

/* Temperatures Packet
    Bias: 20 C
    Range: 20-148 C
    Precision: 0.5 C
    CompressedValue = (uint8_t)floor((RawValue - 20.0) * 2);
*/
struct Packet_Temps {
    uint8_t IGBT;
    uint8_t Motor;
    uint8_t Coolant_In;
    uint8_t Coolant_Out;
    uint8_t Gearbox;
    // Those two are not included in the compression
    uint8_t BrakeLeft;
    uint8_t BrakeRight;
};

/* Pedals Packet
    Throttle:
        Bias: 0
        Range: 0-100 %
        Precision: 0.5 %
        CompressedValue = (uint8_t)floor(RawValue * 2);
    Brake:
        Bias: 0
        Range: 0-200 Bar
        Precision: 1 Bar
        CompressedValue = (uint8_t)RawValue
*/
struct Packet_Pedals {
    uint8_t Throttle_12;
    uint8_t Brake_Front;
    uint8_t Brake_Rear;
};

/* Wheelspeed Packet
    Bias: 0
    Range: 0-765 rpm
    Precision: 3 rpm
    CompressedValue = (uint8_t)floor(RawValue / 3);
*/
struct Packet_Wheels {
    uint8_t RPM_Front_Left;
    uint8_t RPM_Front_Right;
    uint8_t RPM_Rear_Left;
    uint8_t RPM_Rear_Right;
};

/* VCU Packet
    Not compressed
*/
struct Packet_VCU {
    bool ETD;
    bool BMSA;
    uint8_t MCMS;
    uint16_t EMA;
    uint8_t CDS;
    uint16_t PLS;
    uint16_t Current_Low_Battery;
};

/* IMU Packet
    Not compressed. Full precision
*/
struct Packet_IMU {
    float X;
    float Y;
    float Z;
};

struct TelemetryPacket {
  Packet_Settings Settings;
  Packet_Timestamp Timestamp;
  Packet_Performance Performance;
  Packet_BMS BMS;
  Packet_Temps Temps;
  Packet_Pedals Pedals;
  Packet_Wheels Wheels;
  Packet_VCU VCU;
  Packet_IMU IMU;
};

TelemetryPacket CompressedTelemetry;

// Returns the telemetry packet size based on the SelectiveSampling.
// Maximum telemetry packet may be 36 bytes. 
// Includes the SelectiveSampling and the Timestamp values.
uint8_t SizeFromSettings(uint8_t Set) {
	// Settings byte is always present
	uint8_t Size = 1;
	// Timestamp is always added
	Size += sizeof(Packet_Timestamp);
	Size += (Set & MASK_PERF) * sizeof(Packet_Performance);
	Size +=(Set & MASK_BMS) * sizeof(Packet_BMS);
	Size += (Set & MASK_TEMP) * sizeof(Packet_Temps);
	Size += (Set & MASK_PEDALS) * sizeof(Packet_Pedals);
	Size += (Set & MASK_WHEELS) * sizeof(Packet_Wheels);
	Size += (Set & MASK_VCU) * sizeof(Packet_VCU);
	Size += (Set & MASK_IMU) * sizeof(Packet_IMU);
	return Size;
}

#endif