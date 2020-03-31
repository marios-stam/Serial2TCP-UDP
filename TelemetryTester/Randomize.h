#ifndef RANDOMIZE_H
#define RANDOMIZE_H

// The ++ operator will overflow the values and handle the returning to 0

void RandomizeTelemetry() {
	CompressedTelemetry.Performance.RPM++;
  // Do the same for all compressed telemetry structures found in TelemetryPackets.h
}

void RandomizeBMS() {
	// Increment the first value
	Car.datapack_left_box[0]++;
	// Pyramid increment the rest
	for (uint8_t Index = 1; Index < sizeof(Car.datapack_left_box); Index++) {
		Car.datapack_left_box[Index] = Car.datapack_left_box[Index - 1] + 1;
	}
	Car.datapack_right_box[0]++;
	for (uint8_t Index = 1; Index < sizeof(Car.datapack_right_box); Index++) {
		Car.datapack_right_box[Index] = Car.datapack_right_box[Index - 1] + 1;
	}
}

void Randomize() {

	RandomizeTelemetry();

	RandomizeBMS();

}

#endif
