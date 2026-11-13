// Seeed XIAO ESP32-C3 + Grove Shield, Grove EMG OUT -> A0 (GPIO2)
// CSV: timestamp_us,voltage_mV
const int EMG_PIN = A0;
const uint32_t PERIOD_US = 2000; // 500 Hz
uint32_t next_sample;
void setup() {
  Serial.begin(230400);
  analogReadResolution(12);
  analogSetPinAttenuation(EMG_PIN, ADC_11db);
  next_sample = micros() + PERIOD_US;
}
void loop() {
  uint32_t now = micros();
  if ((int32_t)(now - next_sample) >= 0) {
    next_sample += PERIOD_US;
    uint32_t t = micros();
    int mv = analogReadMilliVolts(EMG_PIN);
    Serial.print(t);
    Serial.print(',');
    Serial.println(mv);
    if ((int32_t)(micros() - next_sample) >= 0) next_sample = micros() + PERIOD_US;
  }
}
