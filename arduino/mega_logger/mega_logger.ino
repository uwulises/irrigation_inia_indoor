#include <ArduinoJson.h>
#include <SDI12.h>
#include "HX711.h"


JsonDocument doc;

const unsigned long msgsend = 300000;  // Time between messages in milliseconds (300 second)
unsigned long startTime;
unsigned long lastMsg;
unsigned long riego_litros_timer;
unsigned long tiempo_riego;
String inputString = "";      // a String to hold incoming data
bool stringComplete = false;  // whether the string is complete
volatile unsigned long count0 = 0;
volatile unsigned long count1 = 0;
String selector;
String liters;
String time;
#define solenoide_0 5
#define solenoide_1 6
#define flowpin0 2
#define flowpin1 3
#define sensor_humedad_suelo_0 A2
#define sensor_humedad_suelo_1 A3
#define sensor_humedad_suelo_2 A4
#define sensor_radiacion A5
#define atmos 4
#define lisimetro_sck 8
#define lisimetro_dout 9

HX711 lisimetro_celda;

int moist0 = 0;
int moist1 = 0;
int moist2 = 0;
int radiation = 0;
float lisimetro = 0;
int temperature = 0;
int hr = 0;


void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

void flow0Interrupt() {
  count0++;
}
void flow1Interrupt() {
  count1++;
}
void read_sensors_json(){

  moist0 = analogRead(sensor_humedad_suelo_0);
  moist1 = analogRead(sensor_humedad_suelo_1);
  moist2 = analogRead(sensor_humedad_suelo_2);
  radiation = analogRead(sensor_radiacion);
  lisimetro = (lisimetro_celda.get_units(5)*0.0255)-20.82 > 0 ? (lisimetro_celda.get_units(5)*0.0255)-20.82 : 0;
  temperature = 0;
  hr = 0;
  doc["Sensor humedad suelo 0"] = moist0;
  doc["Sensor humedad suelo 1"] = moist1;
  doc["Sensor humedad suelo 2"] = moist2;
  doc["Sensor radiacion [V]"] = radiation;
  doc["Lisimetro"] = lisimetro;
  doc["Sensor temperatura"] = temperature;
  doc["Sensor humedad relativa"] = hr;
}

void solenoid_state(String selector){
  if (selector == "11"){
    digitalWrite(solenoide_0, LOW);
    delay(100);
    digitalWrite(solenoide_1, LOW);
    delay(100);
  }
  if (selector == "00"){
    digitalWrite(solenoide_0, LOW);
    delay(100);
  }
  if (selector == "01"){
    digitalWrite(solenoide_1, LOW);
    delay(100);
  }
}

void riego_litros(int totalpulseCount, String selector){
  riego_litros_timer = millis();
  if (selector == "11"){
    while (count0 < totalpulseCount && count1 < totalpulseCount){
    }
    doc["Tiempo regado 0"] = (millis() - riego_litros_timer)/1000;
    doc["Tiempo regado 1"] = (millis() - riego_litros_timer)/1000;
  }
  if (selector == "00"){
    while (count0 < totalpulseCount){
    }
    doc["Tiempo regado 0"] = (millis() - riego_litros_timer)/1000;
  }
  if (selector == "01"){
    while (count1 < totalpulseCount){
    }
    doc["Tiempo regado 1"] = (millis() - riego_litros_timer)/1000;
  }

}

void riego_tiempo(unsigned long tiempo_riego){
  while (millis() - startTime < tiempo_riego){
  }
}

void riego(String selector, String liters, String time){
  startTime = millis();
  Serial.print(selector);
  Serial.print(liters);
  Serial.println(time);
  //clear pulse count
  count0 = 0;
  count1 = 0;
  //string to int
  int litros = liters.toInt();
  tiempo_riego = time.toInt()*1000;
  Serial.print("Tiempo riego millis: ");
  Serial.println(tiempo_riego);


  //convert litros to pulse Count (each pulse 2.25 ml)
  int totalpulseCount = litros*444;

  //turn on solenoid
  solenoid_state(selector);

  //check by liters or time
  if (litros>0){
    Serial.println("Riego por litros");
    riego_litros(totalpulseCount, selector);
  }
  if (tiempo_riego>0){
    Serial.println("Riego por tiempo");
    riego_tiempo(tiempo_riego);
    doc["Tiempo regado 0"] = tiempo_riego/1000;
  }

  //count to liters
  doc["Litros regados 0"] = count0/444;
  doc["Litros regados 1"] = count1/444;
  Serial.println(count0);
  Serial.println(count1);
  digitalWrite(solenoide_0, HIGH);
  digitalWrite(solenoide_1, HIGH);
  //reset pulse count
  count0 = 0;
  count1 = 0;

}

void setup() {
  Serial.begin(9600);
  pinMode(A2, INPUT);  // Sensor humedad suelo 0
  pinMode(A3, INPUT);  // Sensor humedad suelo 1
  pinMode(A4, INPUT);  // Sensor humedad suelo 2
  pinMode(A5, INPUT);  // Sensor radiacion [V]
  pinMode(solenoide_0, OUTPUT);  // Solenoide 0
  pinMode(solenoide_1, OUTPUT);  // Solenoide 1
  digitalWrite(solenoide_0, HIGH);
  digitalWrite(solenoide_1, HIGH);
  attachInterrupt(digitalPinToInterrupt(flowpin0), flow0Interrupt, RISING);
  attachInterrupt(digitalPinToInterrupt(flowpin1), flow1Interrupt, RISING);
  lisimetro_celda.begin(lisimetro_dout, lisimetro_sck);
  lisimetro_celda.set_scale();
  delay(1000);
  inputString.reserve(200);
}



void loop() {
  startTime = millis();

  if (startTime - lastMsg > msgsend) {
    read_sensors_json();
    serializeJson(doc, Serial);
    Serial.println();
    lastMsg = startTime;
  }
  if (stringComplete) {
    //take substring from "REG_S00_L0000_T0000\n"
    if (inputString.substring(0,3) == "REG"){
      selector = inputString.substring(5,7);
      liters = inputString.substring(9,13);
      time = inputString.substring(15,19);
      riego(selector, liters, time);
    }
    // clear the string:
    inputString = "";
    stringComplete = false;
  }
  
}
