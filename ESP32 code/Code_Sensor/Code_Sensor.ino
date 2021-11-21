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
#include "SparkFunCCS811.h" //Click here to get the library: http://librarymanager/All#SparkFun_CCS811

#define CCS811_ADDR 0x5B //Default I2C Address
#define LIGHT_PIN   36


#define DHT_PIN 27     // Digital pin connected to the DHT sensor
#define DHTTYPE    DHT11     // DHT 11


enum STEPS{CSS811_SENSOR,DHT_11_SENSOR,GROOVE_LIGHT_SENSOR,SENDING_DATA};
STEPS OneByOne;


struct sensors_Reading
{
  int CO2;
  int tVTOC;
  float humi;
  float temp;
  int   light;
}Values;


CCS811 mySensor(CCS811_ADDR);
DHT dht(DHT_PIN, DHTTYPE);

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
}

void loop()
{
  //Check to see if data is ready with .dataAvailable()

  
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

  delay(1000); 
}
