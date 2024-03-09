
#include <Servo.h>
#include <FastLED.h>
#include "Arduino.h"
#include "ESP8266WiFi.h"
#include "ESP8266WebServer.h"
#include "mdp.h"


#define NUM_LEDS 5

Servo ServoMotTrans;  // create a servo object
Servo ServoMotTilt;  // create a servo object
CRGB leds[NUM_LEDS];

const int servoTransPin = 1; 
const int servoTiltPin = 2; 
const int mainLEDPin = 3; 
const int secRLedPin = 8;
const int secGLedPin = 12;
const int secBLedPin = 13;
const int ringLedPin = 4;

int mainLedRange[] = {2,60};
float transMotorRange[] = {10,70};
float tiltMotorRange[] = {10,50};

long timer = 0;

int ringMode = 0;
int mainLedCount = 0;


//objet webserver
ESP8266WebServer serverWeb(80);


void setup() {
    Serial.begin(115200);
    Serial.println("bonjour ! ");
  	FastLED.addLeds<NEOPIXEL, ringLedPin>(leds, NUM_LEDS);
  	ServoMotTrans.attach(servoTransPin); // attaches the servo on pin 9 to the servo object
  	ServoMotTilt.attach(servoTiltPin);
  	pinMode(mainLEDPin, OUTPUT);
  	pinMode(secRLedPin, OUTPUT);
  	pinMode(secGLedPin, OUTPUT);
  	pinMode(secBLedPin, OUTPUT);
    Serial.println(SSID);
    
    IPAddress ip(192,168,1,110);
    IPAddress gateway(192,168,1,254);
    IPAddress dns(192,168,1,254);
    IPAddress subnet(255,255,255,0);
    WiFi.hostname("GLaDOS");
    //mode de connection
    WiFi.mode(WIFI_STA);
    WiFi.config(ip, gateway, subnet, dns);
    WiFi.begin(SSID, PASSWORD);
  
    static WiFiEventHandler onConnectedHandler = WiFi.onStationModeConnected(onConnected);
    static WiFiEventHandler onGotIPHandler = WiFi.onStationModeGotIP(onGotIP);

    
    serverWeb.on("/test", test);
    serverWeb.begin();
}

void loop() {
    if (WiFi.isConnected()){
        serverWeb.handleClient();
    }
    
    ring();
    secLed((timer/1000)%4 +1);
    Serial.println(String((timer%1000)/10));

    if (mainLedCount == 0){
        mainLedCount = random(30,200);
        mainLed(random(0,100));
    }else mainLedCount--;
    
    //secLed(2);
    tiltMot(0);
    delay(1000);
    tiltMot(100);
    delay(1000);

    timer++;
}

void test(){
    Serial.println("test");  
}

//connection au wifi
void onConnected(const WiFiEventStationModeConnected& event){
    Serial.println("WiFi connected !");
}
void onGotIP(const WiFiEventStationModeGotIP& event){
    Serial.println("Adresse IP : " + WiFi.localIP().toString());
    Serial.print("Puissance de reception : ");
    Serial.println(WiFi.RSSI());
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
        leds[(timer/40)%5] = col;
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
