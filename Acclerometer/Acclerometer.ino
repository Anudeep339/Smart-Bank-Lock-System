const int xPin   = A2;
const int yPin   = A1;
const int zPin   = A0;

boolean buttonState = LOW; 
int buttonPin = 7;
int x = 0;
int y = 0;
int z = 0;

const int ledPin =  13;     
int ledState = LOW;

int pressed=0;

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, INPUT);
}

void loop() {

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

/*Serial.print("X = ");
Serial.println(x);
Serial.print("Y = ");
Serial.println(y);
Serial.print("Z = ");
Serial.println(z);*/

  Serial.println(map(x, 398 , 335, 0, 90));  
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

