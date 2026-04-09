// #include <Arduino_RouterBridge.h>

// const int phPin = A0;
// float pHValue = 0;

// void setup() {
//   // Initialize Bridge at 115200 for Python communication
//   Bridge.begin(115200);
  
//   // Register the function
//   Bridge.provide("get_ph", read_ph_sensor);

//   Monitor.println("Sensor PH-4502C iniciado...");
// }

// void loop() {
//   // Must keep this to listen for Python requests
//   Bridge.update();
// }

// // The "interior" stays float, and we return the result to the Bridge
// float read_ph_sensor() {
//   int sensorValue = analogRead(phPin);
  
//   // Interior float math
//   float voltage = sensorValue * (5.0 / 1023.0);
  
//   // Calculation (Formula from your snippet)
//   pHValue = 7 - ((voltage - 2.5) / 0.18) +13;
  
//   // Optional: Monitor local check
//   Monitor.print("Lectura pH: ");
//   Monitor.println(pHValue);
  
//   return pHValue; 
// }
