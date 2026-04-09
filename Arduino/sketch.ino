#include <Arduino_RouterBridge.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// Temperature Config
#define ONE_WIRE_BUS 2
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// pH Config
const int phPin = A0;

void setup() {
  Bridge.begin(115200);
  
  // Register both RPC functions
  Bridge.provide("get_temperature", read_temp_sensor);
  Bridge.provide("get_ph", read_ph_sensor);

  sensors.begin();
  Monitor.println("Sistemas listos: Temperatura (Pin 2) y pH (A0)");
}

void loop() {
  // Essential for Bridge communication
  Bridge.update();
}

// --- Temperature Function ---
float read_temp_sensor() {
  sensors.requestTemperatures();
  float tempC = sensors.getTempCByIndex(0);
  
  Monitor.print("Temp Local: ");
  Monitor.println(tempC);
  return tempC; 
}

// --- pH Function (with Smoothing) ---
float read_ph_sensor() {
  float totalValue = 0;
  int samples = 10;

  // Average 10 readings to stop the jumping values
  for (int i = 0; i < samples; i++) {
    totalValue += analogRead(phPin);
    delay(5); 
  }
  
  float avgValue = totalValue / samples;
  float voltage = avgValue * (5.0 / 1023.0);
  
  // Using your specific formula +13 offset
  float pHValue = 7 - ((voltage - 2.5) / 0.18) + 8;
  
  // Keep it within real pH limits
  if (pHValue < 0) pHValue = 0;
  if (pHValue > 14) pHValue = 14;

  Monitor.print("pH Local: ");
  Monitor.println(pHValue);
  return pHValue; 
}
