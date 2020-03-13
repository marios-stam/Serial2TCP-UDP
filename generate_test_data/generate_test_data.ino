byte test[100] = {0};

void setup() {
  Serial.begin(115200);
  for(int i=0;i<100;i++) test[i]=analogRead(A0);//get random data
}
void loop() {
   Serial.write(test, sizeof(test));
   delay(10);
}

