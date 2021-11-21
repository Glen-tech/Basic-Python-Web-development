/******************************************************************************
  Read basic CO2 and TVOCs

  Marshall Taylor @ SparkFun Electronics
  Nathan Seidle @ SparkFun Electronics

  April 4, 2017

  https://github.com/sparkfun/CCS811_Air_Quality_Breakout
  https://github.com/sparkfun/SparkFun_CCS811_Arduino_Library

  Read the TVOC and CO2 values from the SparkFun CSS811 breakout board

  A new sensor requires at 48-burn in. Once burned in a sensor requires
  20 minutes of run in before readings are considered good.

  Hardware Connections (Breakoutboard to Arduino):
  3.3V to 3.3V pin
  GND to GND pin
  SDA to A4
  SCL to A5

******************************************************************************/
#include <Wire.h>
#include <math.h>
#include <DHT.h>
#include <WiFi.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>

#include "SparkFunCCS811.h" //Click here to get the library: http://librarymanager/All#SparkFun_CCS811

#define CCS811_ADDR 0x5B //Default I2C Address
#define LIGHT_PIN   36


#define DHT_PIN 27     // Digital pin connected to the DHT sensor
#define DHTTYPE    DHT11     // DHT 11


enum STEPS{CSS811_SENSOR,DHT_11_SENSOR,GROOVE_LIGHT_SENSOR,SENDING_DATA} OneByOne;

struct sensors_Reading
{
  int CO2;
  int tVTOC;
  float humi;
  float temp;
  int   light;
}Values;

struct sensors_Reading_string
{
  String sCO2;
  String stVTOC;
  String shumi;
  String stemp;
  String slight;
}sValues;


CCS811 mySensor(CCS811_ADDR);
DHT dht(DHT_PIN, DHTTYPE);

WiFiClient client;
HTTPClient http;

const char* ssid = "Enter here";
const char* password = "Enter here";

//Your Domain name with URL path or IP address with path
const char* serverName = "http://192.168.0.223:8000";


void css811_sensor()
{
  if (mySensor.dataAvailable())
  {
    //If so, have the sensor read and calculate the results.
    //Get them later
    mySensor.readAlgorithmResults();
    Values.CO2 = mySensor.getCO2();
    Values.tVTOC = mySensor.getTVOC();
  }
}
void DHT11_sensor()
{
    Values.humi = dht.readHumidity();
    Values.temp = dht.readTemperature();
}

void groove_light_sensor()
{
    Values.light = analogRead(LIGHT_PIN); 
}

void sending_data()
{
  Serial.print("CO2: ");
  Serial.print(Values.CO2);
  Serial.print("tVOC: ");
  Serial.println(Values.tVTOC);

  Serial.print("Temperature: ");
  Serial.print(Values.temp);
  Serial.print("ºC ");
  Serial.print("Humidity: ");
  Serial.println(Values.humi);  

  Serial.print("Light analoge read: ");
  Serial.println(Values.light);

  sValues.sCO2 = String(Values.CO2);
  sValues.stVTOC = String(Values.tVTOC);
  sValues.shumi = String(Values.humi);
  sValues.stemp = String(Values.temp);
  sValues.slight= String(Values.light);


  StaticJsonDocument<300> doc;

  JsonArray data_CSS811 = 
  doc.createNestedArray("CSS811 Sensor");
  data_CSS811.add("Value CO2");
  data_CSS811.add(sValues.sCO2);
  data_CSS811.add("Value tVTOC");
  data_CSS811.add(sValues.stVTOC);

  JsonArray data_DHT11 =
  doc.createNestedArray("DHT11 Sensor");
  data_DHT11.add("Value humidity");
  data_DHT11.add(sValues.shumi);
  data_DHT11.add("Value temperature");
  data_DHT11.add(sValues.stemp);

  JsonArray data_Groove =
  doc.createNestedArray("Groove light sensor");
  data_Groove.add("Value light");
  data_Groove.add(sValues.slight);
 
  // Your Domain name with URL path or IP address with path
  http.begin(client, serverName);
  http.addHeader("Content-Type", "application/json");

  String requestBody;
  serializeJson(doc, requestBody);
  int httpResponseCode = http.POST(requestBody);
 
     
  Serial.print("HTTP Response code: ");
  Serial.println(httpResponseCode);
        
  // Free resources
  http.end();

  
}

void setup()
{
  Serial.begin(9600);
  Serial.println("Reading sensor data and sending ESP32");

  Wire.begin(); //Inialize I2C Hardware

  dht.begin();

  if (mySensor.begin() == false)
  {
    Serial.print("Problem sensors. Please check wiring. Freezing...");
    while (1);
  }

  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
 
  Serial.println("Timer set to 5 seconds (timerDelay variable), it will take 5 seconds before publishing the first reading.");
}

void loop()
{
  
    if(WiFi.status() == WL_CONNECTED)
      {
            switch(OneByOne)
            {
                case CSS811_SENSOR: 
                css811_sensor();
                OneByOne=DHT_11_SENSOR;
                break;
            
            
                case DHT_11_SENSOR: 
                DHT11_sensor();
                OneByOne=GROOVE_LIGHT_SENSOR;
                break;
            
                case GROOVE_LIGHT_SENSOR: 
                groove_light_sensor();
                OneByOne= SENDING_DATA;
                break;
            
                case SENDING_DATA: 
                sending_data();
                OneByOne=CSS811_SENSOR;
                break;
            
                default: Serial.println("Something went wrong");
                }
  
    }

      else 
      {
            Serial.println("WiFi Disconnected");
            Serial.println("WiFi Resconnecting");
            
              while(WiFi.status() != WL_CONNECTED)
              {
              delay(500);
              Serial.print(".");
              }
      }

  delay(1000);
  
  
 }
