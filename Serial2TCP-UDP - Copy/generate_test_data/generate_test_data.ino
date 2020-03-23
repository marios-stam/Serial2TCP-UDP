byte test[100] = {0};

void setup() {
  Serial.begin(115200);
  for(int i=0;i<100;i++) {
    test[i]=i;//get random data
    //Serial.println(test[i]);
  }
  //sizeof(test)=100
}
void loop() {
   Serial.write(test, sizeof(test));
   delay(10);
}

