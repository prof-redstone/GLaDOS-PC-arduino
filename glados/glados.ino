
#include <Servo.h>
#include <FastLED.h>
#define NUM_LEDS 5

Servo ServoMotTrans;  // create a servo object
Servo ServoMotTilt;  // create a servo object
CRGB leds[NUM_LEDS];

const int servoTransPin = 9; 
const int servoTiltPin = 10; 
const int mainLEDPin = 11; 
const int secRLedPin = 8;
const int secGLedPin = 12;
const int secBLedPin = 13;
const int ringLedPin = 7;

int mainLedRange[] = {2,60};
float transMotorRange[] = {10,70};
float tiltMotorRange[] = {10,50};

long time = 0;

int ringMode = 0;
int mainLedCount = 0;


void setup() {
    Serial.begin(9600);
	FastLED.addLeds<NEOPIXEL, ringLedPin>(leds, NUM_LEDS);
	ServoMotTrans.attach(servoTransPin); // attaches the servo on pin 9 to the servo object
	ServoMotTilt.attach(servoTiltPin);
	pinMode(mainLEDPin, OUTPUT);
	pinMode(secRLedPin, OUTPUT);
	pinMode(secGLedPin, OUTPUT);
	pinMode(secBLedPin, OUTPUT);
}

void loop() {
    ring();
    secLed((time/1000)%4 +1);
    Serial.println(String((time%1000)/10));

    if (mainLedCount == 0){
        mainLedCount = random(30,200);
        mainLed(random(0,100));
    }else mainLedCount--;
    
    //secLed(2);
    tiltMot((time%1000)/10);

    time++;
}

void ring(){
    float lum = 1.0;
    CRGB col = CRGB::Yellow;
    col = CRGB(255*lum,0*lum,0*lum);

    if(ringMode == 0){
        for (int i = 0; i < NUM_LEDS; i++){
            leds[i] = col;
        }
    }
    if(ringMode == 1){
        for (int i = 0; i < NUM_LEDS; i++){
            leds[i] = CRGB::Black;
        }
        leds[(time/40)%5] = col;
    }

    FastLED.show();
}

void tiltMot(int ang){
    if(ang < 0 || ang > 100) return;
    ServoMotTilt.write(((float)ang/100.)*tiltMotorRange[0] + (1 - (float)ang/100.)*tiltMotorRange[1]);
}

void transMot(int ang){
    if(ang < 0 || ang > 100) return;
    ServoMotTrans.write(((float)ang/100.)*transMotorRange[0] + (1 - (float)ang/100.)*transMotorRange[1]);
}

void mainLed(int pow){
    int val = (int)(((float)pow/100.)*mainLedRange[0] + (1 - (float)pow/100.)*mainLedRange[1]);
    analogWrite(mainLEDPin, val);
}

void secLed(int col){
	//0black 1red 2green 3blue 4yellow
	if(col == 0){
        digitalWrite(secRLedPin, LOW);
        digitalWrite(secGLedPin, LOW);
        digitalWrite(secBLedPin, LOW);
	}if(col == 1){
        digitalWrite(secRLedPin, HIGH);
        digitalWrite(secGLedPin, LOW);
        digitalWrite(secBLedPin, LOW);
	}if(col == 2){
        digitalWrite(secRLedPin, LOW);
        digitalWrite(secGLedPin, HIGH);
        digitalWrite(secBLedPin, LOW);
	}if(col == 3){
        digitalWrite(secRLedPin, LOW);
        digitalWrite(secGLedPin, LOW);
        digitalWrite(secBLedPin, HIGH);
	}if(col == 4){
        digitalWrite(secRLedPin, HIGH);
        digitalWrite(secGLedPin, HIGH);
        digitalWrite(secBLedPin, LOW);
	}
    return;
}
