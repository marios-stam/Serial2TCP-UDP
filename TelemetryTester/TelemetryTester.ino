#include "Car.h"

#include "Definitions.h"
#include "TelemetryPackets.h"
#include "Randomize.h"

void setup() {

	// Initialize communication with the telemetry host
	InitXBee();

	// Initialize the onboard indicator
	InitIndicator();

}

void loop() {

	// Handle communication with the telemetry host
	HandleXBee();

	// Handle the toggling of the onboard indicator
	HandleIndicator();

	// Create the random data to feed the GUI
	//Randomize();

}
