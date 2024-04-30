
#include <Servo.h>
#include <FastLED.h>
#include "Arduino.h"
#include "ESP8266WebServer.h"
#include "mdp.h"


#define NUM_LEDS 5

Servo ServoMotTrans;  // create a servo object
Servo ServoMotTilt;  // create a servo object
Servo ServoMotTurn;  // create a servo object
CRGB leds[NUM_LEDS];

const int servoTransPin = 14; 
const int servoTiltPin = 12; 
const int servoTurnPin = 4; 
const int mainLEDPin = 9; 
const int secRLedPin = 5;
const int secGLedPin = 0;
const int secBLedPin = 2;
const int ringLedPin = 3;

int mainLedRange[] = {0,230};
float transMotorRange[] = {0,180};
float tiltMotorRange[] = {5,175};
float turnMotorRange[] = {5,175};

long timer = 0;

int ringMode = 0;
int mainLedCount = 0;
int mainLedMode = 0;//0 static light, 1 talk mode
int ringColor[] = {0,0,0};

float speedTurnMot = 4.;
float targetTurnMotPos = turnMotorRange[0];
float currentTurnMotPos = turnMotorRange[0];


float speedTransMot = 9.;
float targetTransMotPos = transMotorRange[0];
float currentTransMotPos = transMotorRange[0];


//objet webserver
ESP8266WebServer serverWeb(80);


void setup() {
    Serial.begin(115200);
    Serial.println("GLaDOS ESP8266 ip 192.168.1.111");
  	FastLED.addLeds<NEOPIXEL, ringLedPin>(leds, NUM_LEDS);
  	ServoMotTrans.attach(servoTransPin); // attaches the servo on pin 9 to the servo object
  	ServoMotTilt.attach(servoTiltPin);
    ServoMotTurn.attach(servoTurnPin);
  	pinMode(mainLEDPin, OUTPUT);
  	pinMode(secRLedPin, OUTPUT);
  	pinMode(secGLedPin, OUTPUT);
  	pinMode(secBLedPin, OUTPUT);
    Serial.println(SSID);
    
    IPAddress ip(192,168,1,111);
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
    serverWeb.on("/ping", ping);
    serverWeb.on("/api", handleAPI);
    serverWeb.on("/stop", stop);
    serverWeb.begin();
}

void loop() {
    if (WiFi.isConnected()){
        serverWeb.handleClient();
        
        ring();
        updateMot();

        if(mainLedMode == 1){
          if (mainLedCount == 0){
              mainLedCount = random(1,20);
              mainLed(random(mainLedRange[0],mainLedRange[1]));
          }else {
            mainLedCount--;
          }
        }
        
        timer++;
    }else{
        secLed(3);//attente de connection 
        delay(100);
        secLed(0);
        delay(100);
    }
}

void test(){
    Serial.println("test");  
    secLed(2);
}

void ping(){
    Serial.println("ping");  
    serverWeb.send(200, "text/plain", "pong");
}

void stop(){
    serverWeb.stop();
    secLed(2);
}

void handleAPI(){
    String reponse;
    //http://192.168.1.111/api?Turn=50
    if (serverWeb.args() > 0){
        Serial.println(serverWeb.argName(0));
        Serial.println(serverWeb.arg(0));
        
        if (serverWeb.argName(0) == "SecLed"){
            Serial.println("changement de secLed ");
            int rep = serverWeb.arg(0).toInt();
            secLed(rep);
        }
        if (serverWeb.argName(0) == "Tilt"){
            Serial.println("changement de Tilt ");
            int rep = serverWeb.arg(0).toInt();
            if(rep >= 0 && rep <= 100){
                tiltMot(rep);
            }
        }
        if (serverWeb.argName(0) == "Trans"){
            Serial.println("changement de Trans ");
            int rep = serverWeb.arg(0).toInt();
            if(rep >= 0 && rep <= 100){
                transMot(rep);
            }
        }
        if (serverWeb.argName(0) == "Turn"){
            Serial.println("changement de Turn ");
            int rep = serverWeb.arg(0).toInt();
            if(rep >= 0 && rep <= 100){
                turnMot(rep);
            }
        }
        if (serverWeb.argName(0) == "MainLed"){
            Serial.println("changement de mainLed ");
            int rep = serverWeb.arg(0).toInt();
            if(rep >= 0 && rep <= 100){
              mainLedMode = 0;
              mainLed(rep);
            }else if(rep = -1){
              mainLedMode = 1;
            }
        }
        if (serverWeb.argName(0) == "RingCol"){
            Serial.println("changement de couleur du ring ");
            int index = 0;
            String str = serverWeb.arg(0);
            while (str.length() > 0 && index < 3) {
                int commaIndex = str.indexOf('_');
                if (commaIndex != -1) {
                ringColor[index] = str.substring(0, commaIndex).toInt();
                str = str.substring(commaIndex + 1);
                } else {
                    ringColor[index] = str.toInt();
                }
                index++;
            }
        }
        if (serverWeb.argName(0) == "Speed"){
            float rep = serverWeb.arg(0).toFloat();
            speedTransMot = rep;
            
        }
        
    }else{
        reponse = "need arg";
        serverWeb.send(200, "text/plain", reponse);
    }
    
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

void updateMot(){
    float epsilon = 2*speedTurnMot;
    if(abs(targetTurnMotPos - currentTurnMotPos) > epsilon ){
        if(targetTurnMotPos - currentTurnMotPos > 0){
            currentTurnMotPos += speedTurnMot;
        }else{
            currentTurnMotPos -= speedTurnMot;
        }
    }
    
    epsilon = 2*speedTransMot;
    if(abs(targetTransMotPos - currentTransMotPos) > epsilon ){
        if(targetTransMotPos - currentTransMotPos > 0){
            currentTransMotPos += speedTransMot;
        }else{
            currentTransMotPos -= speedTransMot;
        }
    }
    ServoMotTrans.write(currentTransMotPos);
    ServoMotTurn.write(currentTurnMotPos);
}


void ring(){
    float lum = 1.0;
    CRGB col = CRGB(ringColor[0]*lum,ringColor[1]*lum,ringColor[2]*lum);

    if(ringMode == 0){
        for (int i = 0; i < NUM_LEDS; i++){
            leds[i] = col;
        }
    }
    if(ringMode == 1){
        for (int i = 0; i < NUM_LEDS; i++){
            leds[i] = CRGB::Black;
        }
    }

    FastLED.show();
}

void tiltMot(int ang){
    if(ang < 0 || ang > 100) return;
    float val = ((float)ang/100.)*tiltMotorRange[1] + (1 - (float)ang/100.)*tiltMotorRange[0];
    ServoMotTilt.write(val);
}

void turnMot(int ang){
    if(ang < 0 || ang > 100) return;
    float val = ((float)ang/100.)*turnMotorRange[1] + (1 - (float)ang/100.)*turnMotorRange[0];
    targetTurnMotPos = val;
    //ServoMotTurn.write(val);
}

void transMot(int ang){
    if(ang < 0 || ang > 100) return;
    float val = ((float)ang/100.)*transMotorRange[1] + (1 - (float)ang/100.)*transMotorRange[0] ;
    targetTransMotPos = val;
}

void mainLed(int pow){
    int val = (int)(((float)pow/100.)*mainLedRange[1] + (1 - (float)pow/100.)*mainLedRange[0]);
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
