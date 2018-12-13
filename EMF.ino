#define NUMREADINGS 15

int senseLimit = 15;
int val = 0;
int probePin = val;

//const int sensorPin = A2;
//const int lightSensor = A4;
int lightVal;
int sensorLow = 1023;
int sensorHigh = 0;


int LED1 = 2;
int LED2 = 3;
int LED3 = 4;
int LED4 = 5;
int LED5 = 6;
int LED6 = 7;
int LED7 = 8;
int buzzer = 13;
int buzzerTone = 0;
unsigned long previousMillis = 0; const long interval = 1000;
int readings[NUMREADINGS];
int index = 0;
int total = 0;
int average = 0;
int buzzVal = 0;
void setup() {
pinMode(2, OUTPUT);

pinMode(3, OUTPUT);

pinMode(4, OUTPUT);

pinMode(5, OUTPUT);

pinMode(6, OUTPUT);

pinMode(7, OUTPUT);

pinMode(8, OUTPUT);

pinMode(13, OUTPUT);

Serial.begin(9600);

for (int i = 0; i < NUMREADINGS; i++) readings[i] = 0;
}



void loop() {
/*  
while (millis() < 4000) {
  lightVal = analogRead(lightSensor);
  if(lightVal > sensorHigh) {
    sensorHigh = lightVal;
  }
  if(lightVal < sensorLow) {
    sensorLow = lightVal;
  }
}
lightVal = analogRead(lightSensor);
Serial.print("Light Level = ");
Serial.print(lightVal);
Serial.println();
  

int tempIn = analogRead(sensorPin);

float voltage = (tempIn/1024.0) * 5.0;

float temperature = (voltage - .5) * 100;
Serial.print("Temperature = ");
Serial.print(temperature);
Serial.println();*/
val = analogRead(probePin);
if(val >= 1){
  val = constrain(val, 1, senseLimit); val = map(val, 1, senseLimit, 1, 1023);
  total -= readings[index];
  readings[index] = val;
  total += readings[index];
  index = (index + 1);
  
  if (index >= NUMREADINGS) index = 0;
  average = total / NUMREADINGS;
  
  if (average < 150) {digitalWrite(LED7, HIGH); tone(buzzer, 1500);} else {digitalWrite(LED7, LOW);}
   
  if (average < 300) {digitalWrite(LED6, HIGH);} else {digitalWrite(LED6, LOW);}
  
  if (average < 450) {digitalWrite(LED5, HIGH);} else {digitalWrite(LED5, LOW);}
  
  if (average < 600) {digitalWrite(LED4, HIGH);} else {digitalWrite(LED4, LOW); noTone(buzzer);}
  
  if (average < 750) {digitalWrite(LED3, HIGH);} else {digitalWrite(LED3, LOW);}
  
  if (average < 900) {digitalWrite(LED2, HIGH);} else {digitalWrite(LED2, LOW);}
  
  if (average <= 1023) {digitalWrite(LED1, HIGH);} else {digitalWrite(LED1, LOW);}
  
  Serial.print("EMF Value: ");
  Serial.print(val); // use output to aid in calibrating}
  Serial.println();
  Serial.println("nl"); 
  
  
}


}
