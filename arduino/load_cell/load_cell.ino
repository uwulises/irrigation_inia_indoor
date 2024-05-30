#include <SPI.h>
#include "HX711.h"

#define DT1 2
#define SCK1 3
#define DT2 4
#define SCK2 5
#define DT3 6
#define SCK3 7
#define DT4 8
#define SCK4 9

HX711 celda1;
HX711 celda2;
HX711 celda3;
HX711 celda4;
float valor1=0.0;
float valor2=0.0;
float valor3=0.0;
float valor4=0.0;
float suma=0.0;

String inputString = "";
bool stringComplete = false;

void serialEvent()
{
    while (Serial.available())
    {
        // get the new byte:
        char inChar = (char)Serial.read();
        // add it to the inputString:
        inputString += inChar;
        // if the incoming character is a newline, set a flag so the main loop can
        // do something about it:
        if (inChar == '\n')
        {
            stringComplete = true;
        }
    }
}

void take_measure()
{
    valor1 = celda1.get_units(10);
    valor2 = celda2.get_units(10);
    valor3 = celda3.get_units(10);
    valor4 = celda4.get_units(10);
    suma = valor1 + valor2 + valor3 + valor4;
    Serial.print("SumaV1V2V3V4");
    Serial.print(",");
    Serial.print(suma);
    Serial.print(",");
    Serial.print(valor1);
    Serial.print(",");
    Serial.print(valor2);
    Serial.print(",");
    Serial.print(valor3);
    Serial.print(",");
    Serial.println(valor4);
}

void setup()
{
    Serial.begin(115200);
    celda1.begin(DT1, SCK1);
    celda1.set_scale(205.3);
    celda1.tare();
    celda2.begin(DT2, SCK2);
    celda2.set_scale(208.1);
    celda2.tare();
    celda3.begin(DT3, SCK3);
    celda3.set_scale(212);
    celda3.tare();
    celda4.begin(DT4, SCK4);
    celda4.set_scale(206.7);
    celda4.tare();
    delay(1000);
}

void loop()
{

    if (stringComplete)
    {
        if (inputString == "MEAS\n")
        {
            take_measure();
        }
        inputString = "";
        stringComplete = false;
    }
}
