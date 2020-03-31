#define TelemetryTX 10//marios change from 5
#define Telemetry2TX 150//marios change from 150

unsigned long LastTelemetryTX = 0;
unsigned long LastTelemetry2TX = 0;

//const extern uint8_t ID_SEND_TELEMETRY = 6;

//const uint8_t PacketStartByte = 0x02;
//const uint8_t PacketEndByte = 0x03;

void InitXBee() {
    XBee.begin(115200);
}

// Based on the SelectiveSampling setting put the values into telemetry
// packet(s) and transmit them to the host.
void SendTelemetry() {

	// Create the array based on the SelectiveSampling setting
	uint8_t Setting = B01111111; //CompressedTelemetry.Settings.SelectiveSampling;
	byte Tmp[SizeFromSettings(Setting)];

	// Variable to keep track of the array's index
	uint8_t ind = 0;
	// Put the SelectiveSampling setting into the packet
	Tmp[ind++] = Setting;

	// Keep track of the index of the packet with a static variable
	static uint32_t Index = 0;
	++Index;
	CompressedTelemetry.Timestamp.IndexMSB = Index >> 16;
	CompressedTelemetry.Timestamp.IndexMMSB = Index >> 8;
	CompressedTelemetry.Timestamp.IndexLSB = Index;

	// Put the Timestamp information and increment the index
	memcpy(&Tmp[ind], &CompressedTelemetry.Timestamp, sizeof(Packet_Timestamp));
	ind += sizeof(Packet_Timestamp);
	// ind should be 7 by this time

	// Based on the SelectiveSampling put the appropriate values into the packet
	if (Setting & MASK_PERF) {
		memcpy(&Tmp[ind], &CompressedTelemetry.Performance, sizeof(Packet_Performance));
		ind += sizeof(Packet_Performance);
	}
	if (Setting & MASK_BMS) {
		memcpy(&Tmp[ind], &CompressedTelemetry.BMS, sizeof(Packet_BMS));
		ind += sizeof(Packet_BMS);
	}
	if (Setting & MASK_TEMP) {
		memcpy(&Tmp[ind], &CompressedTelemetry.Temps, sizeof(Packet_Temps));
		ind += sizeof(Packet_Temps);
	}
	// If all packets are included we are at 33 bytes already

	if (Setting & MASK_PEDALS) {
		memcpy(&Tmp[ind], &CompressedTelemetry.Pedals, sizeof(Packet_Pedals));
		ind += sizeof(Packet_Pedals);
	}

	if (Setting & MASK_WHEELS) {
		memcpy(&Tmp[ind], &CompressedTelemetry.Wheels, sizeof(Packet_Wheels));
		ind += sizeof(Packet_Wheels);
	}
	if (Setting & MASK_VCU) {
		memcpy(&Tmp[ind], &CompressedTelemetry.VCU, sizeof(Packet_VCU));
		ind += sizeof(Packet_VCU);
	}
	if (Setting & MASK_IMU) {
		memcpy(&Tmp[ind], &CompressedTelemetry.IMU, sizeof(Packet_IMU));
		ind += sizeof(Packet_IMU);
	}

	// Transmit the telemetry packet to the host
	byte TX[ind + 1];
	TX[0] = ID_SEND_TELEMETRY;
	memcpy(&TX[1], &Tmp, ind);
	unsigned short crc = crc16(TX, ind + 1);
	XBee.write((byte)PacketStartByte);
	XBee.write((byte)(ind + 1));
	XBee.write(TX, ind + 1);
	XBee.write((byte)(crc >> 8));
	XBee.write((byte)(crc & 0xFF));
	XBee.write((byte)PacketEndByte);

}

void SendTelemetryBMS() {
	uint8_t DatapackLeft = sizeof(Car.datapack_left_box);
	uint8_t DatapackRight = sizeof(Car.datapack_right_box);

	byte Tmp[DatapackLeft + DatapackRight + 2];
	uint8_t ind = 0;

	Tmp[ind++] = DatapackLeft;
	memcpy(&Tmp[ind], &Car.datapack_left_box, DatapackLeft);
	ind += DatapackLeft;

	Tmp[ind++] = DatapackRight;
	memcpy(&Tmp[ind], &Car.datapack_right_box, DatapackRight);
	ind += DatapackRight;

	byte TX[ind + 1];
	TX[0] = ID_SEND_BMS;
	memcpy(&TX[1], &Tmp, ind);
	unsigned short crc = crc16(TX, ind + 1);
	XBee.write((byte)PacketStartByte);
	XBee.write((byte)(ind + 1));
	XBee.write(TX, ind + 1);
	XBee.write((byte)(crc >> 8));
	XBee.write((byte)(crc & 0xFF));
	XBee.write((byte)PacketEndByte);
}

void HandleXBee() {

	// Transmit telemetry data at specified intervals
	if (millis() > LastTelemetryTX + TelemetryTX) {
    RandomizeTelemetry();
		SendTelemetry();
		LastTelemetryTX = millis();
	}

	if (millis() > LastTelemetry2TX + Telemetry2TX) {
      RandomizeBMS();
		  SendTelemetryBMS();
        LastTelemetry2TX = millis();
    }

	// Handle the received data for bidirectional communication
	HandleRX();

}
