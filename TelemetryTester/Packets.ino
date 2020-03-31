// The start and end bytes of the packets
#define PacketStartByte 0x02
#define PacketEndByte 0x03
// The size of the receive buffer
#define RXBuffer 20
// Packet receive timeout
#define RXTimeout 100

// The RX buffer
uint8_t RX[RXBuffer];
uint8_t RXPointer = 0;
// The extracted received data
uint8_t RXData[RXBuffer - 5];
uint8_t RXDataLen = 0;
// Time keeping of the last received byte
unsigned long LastReceived = 0;
// Flag for receive timeout
bool IsWaiting = false;

// Send acknowledgement packet
void SendACK(uint8_t COMM_ID) {
	byte TmpBuf[1] = {COMM_ID};
	SendPacket(TmpBuf, 1);
}

// Create and send packet from given data
void SendPacket(unsigned char *data, unsigned int len) {
	unsigned short crc = crc16(data, len);
	XBee.write((byte)PacketStartByte);
	XBee.write((byte)len);
	XBee.write(data, len);
	XBee.write((byte)(crc >> 8));
	XBee.write((byte)(crc & 0xFF));
	XBee.write((byte)PacketEndByte);
}

void SendPacket(unsigned char *data, unsigned int len, uint8_t ID) {
	uint8_t Dat[len + 1];
	Dat[0] = ID;
	memcpy(&Dat[1], data, len);
	SendPacket(Dat, len + 1);
}

// Execute received command
void ProcessData() {
	switch (RXData[0]) {
		case ID_CONNECTION:
			SendACK(ID_CONNECTION);
			break;
		default:
			break;
	}
}

void ReceiveSuccess() {
	ProcessData();
	ReceiveFailed();
}

void ReceiveFailed() {
	RXPointer = 0;
	RXDataLen = 0;
	IsWaiting = false;
}

void ProcessRX() {
	if (RXPointer > 0) {
		uint8_t len = 0;
		if (RX[0] == PacketStartByte) {
			if (RXPointer >= 2) {
				len = RX[1];
				if (RXPointer == 3) {
					// do check for available command
					// else ReceiveFailed(); due to incorrect command id
				}
				if (RXPointer >= 5 + len) {
					if (RX[4 + len] == PacketEndByte) {
						RXDataLen = 0;
						for (int i = 2; i <= len + 1; i++) {
							RXData[RXDataLen++] = RX[i];
						}
						unsigned short crc = crc16(RXData, RXDataLen);
						if (RX[2 + len] == (uint8_t)(crc >> 8) && RX[3 + len] == (uint8_t)(crc & 0xFF)) {
							ReceiveSuccess();
						} else {
							// Incorrect checksum
							ReceiveFailed();
						}
					} else {
						// Incorrect last packet byte
						ReceiveFailed();
					}
				}
			}
		} else {
			// Incorrect first packet byte
			ReceiveFailed();
		}
	}
}

void HandleRX() {
	// Only process if packets feature is active
	if (XBee.available()) {
		RX[RXPointer++] = XBee.read();
		LastReceived = millis();
		IsWaiting = true;
		if (RXPointer >= RXBuffer) {
			ReceiveFailed();
		}
		ProcessRX();
	} else {
		if (IsWaiting && millis() - LastReceived > RXTimeout) {
			// Timeout
			ReceiveFailed();
		}
	}
}
