const uint8_t PIN_INDICATOR = 13;
const bool PIN_INDICATOR_LOGIC = true;
const int INTERVAL_INDICATOR = 250;

bool IndicatorState = false;

void IndicatorOn() {
	digitalWrite(PIN_INDICATOR, PIN_INDICATOR_LOGIC);
	IndicatorState = true;
}

void IndicatorOff() {
	digitalWrite(PIN_INDICATOR, !PIN_INDICATOR_LOGIC);
	IndicatorState = false;
}

void InitIndicator() {
	pinMode(PIN_INDICATOR, OUTPUT);
	IndicatorOff();
}

void HandleIndicator() {

	// Keep track of the last toggle of the indicator's state
	static unsigned long LastToggle = 0;

	// Toggle the indicator if enough time passed
	if (millis() > LastToggle + INTERVAL_INDICATOR) {
		IndicatorState ? IndicatorOff() : IndicatorOn();
		LastToggle = millis();
	}

}