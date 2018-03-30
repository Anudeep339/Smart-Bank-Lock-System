#include "HX711.h"

#define DOUT  2
#define CLK  3

HX711 scale(DOUT , CLK);

float calibration_factor = 2230; // this calibration factor is adjusted according to my load cell
float units;
float ounces;

const int xPin   = A2;
const int yPin   = A1;
const int zPin   = A0;

boolean buttonState = LOW; 
int buttonPin = 7;
int x = 0;
int y = 0;
int z = 0;

const int ledPin =  13;

void setup() {
  Serial.begin(9600);
  scale.set_scale();
  scale.tare();  //Reset the scale to 0

  long zero_factor = scale.read_average();
  pinMode(buttonPin, INPUT);
}

void loop() {

  scale.set_scale(calibration_factor); //Adjust to this calibration factor
  units = scale.get_units(), 10;
  if (units < 0)
  {
    units = 0.00;
  }
  ounces = units * 0.035274;
  //Serial.print(units);


  x = analogRead(xPin);
  y = analogRead(yPin);
  z = analogRead(zPin);
  
  if(debounceButton(buttonState) == HIGH && buttonState == LOW)
  {
    Serial.print('#');
    buttonState = HIGH;
  }
  else if(debounceButton(buttonState) == LOW && buttonState == HIGH)
  {
    buttonState = LOW;
  }
  
  /*
  Serial.print("X = ");
  Serial.println(x);
  Serial.print("Y = ");
  Serial.println(y);
  Serial.print("Z = ");
  Serial.println(z);*/

  Serial.println(map(x, 404 , 343, 0, 90));
  Serial.print("*");
  Serial.println(units);

  delay(200);
}

boolean debounceButton(boolean state)
{
  boolean stateNow = digitalRead(buttonPin);
  if(state!=stateNow)
  {
    delay(10);
    stateNow = digitalRead(buttonPin);
  }
  return stateNow;
}

