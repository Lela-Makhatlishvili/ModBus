#include <Arduino.h>
#include <WiFi.h>
#include <Adafruit_BMP085.h>
#include <dummy.h>
Adafruit_BMP085 bmp;

WiFiClient wifi_client;

const char* ssid = "Modbus";
const char* password = "Modbus123";

const uint port = 502;
const char* ip = "192.168.0.102";

unsigned short  t_id = 0;
unsigned char   dev_id = 1;

float OldT = 0.0;
float OldH = 0.0;
float OldG = 0.0;

void setup() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  
  pinMode(INPUT, 35);
  bmp.begin();
  
  OldT = GetT();
  send_request_temp(dev_id,(short)OldT);
  OldH = GetH();
  send_request_humidity(dev_id,(short)OldH);
  OldG = GetG();
  send_request_gas_co(dev_id,(short)OldG);
}

float GetT(){
 int value1 = analogRead(33);
  float Volts = (value1 * 5) / 1023.0;
  return  Volts * 100;
}


float GetH(){
  int pr = bmp.readPressure();
  return pr;
}

float GetG(){
  int value =  analogRead(35);
  return value;
}

void loop() {
  float NewT = GetT();
  float NewH = GetH();
  float NewG = GetG();
  
  if(NewT > OldT + 1 || NewT < OldT - 1){
    send_request_temp(dev_id,(short)NewT);
  }
  
  if(NewH > OldH + 1 || NewH < OldH - 1){
    send_request_humidity(dev_id,(short)NewH);
  }
  if(NewG > OldG + 1 || NewG < OldG - 1){
    send_request_gas_co(dev_id,(short)NewG);
  }
  delay(1000);
}

void send_request_temp(unsigned char dev_id, short meaning) {
  if(wifi_client.connected()) {
    return;
  }
  if(!wifi_client.connect(ip, port)) {
    return;
  }
  unsigned char buff[12];
  buff[0] = t_id >> 8;
  buff[1] = t_id & 0xff;
  buff[2] = 0;
  buff[3] = 0;
  buff[4] = 0;
  buff[5] = 6;
  buff[6] = dev_id;
  buff[7] = 0x06;
  buff[8] = 0;
  buff[9] = 0;
  buff[10] = meaning >> 8;
  buff[11] = meaning & 0xff;
  
  wifi_client.write(buff, 12);
  
  if(wifi_client.available() > 0) {
    wifi_client.read(buff, 12);
  }
  t_id++;
  wifi_client.stop();
}

void send_request_humidity(unsigned char dev_id, short meaning) {
  if(wifi_client.connected()) {
    return;
  }
  if(!wifi_client.connect(ip, port)) {
    return;
  }
  unsigned char buff[12];
  buff[0] = t_id >> 8;
  buff[1] = t_id & 0xff;
  buff[2] = 0;
  buff[3] = 0;
  buff[4] = 0;
  buff[5] = 6;
  buff[6] = dev_id;
  buff[7] = 0x06;
  buff[8] = 0;
  buff[9] = 1;
  buff[10] = meaning >> 8;
  buff[11] = meaning & 0xff;
  
  wifi_client.write(buff, 12);
  
  if(wifi_client.available() > 0) {
    wifi_client.read(buff, 12);
  }
  t_id++;
  wifi_client.stop();
}

void send_request_gas_co(unsigned char dev_id, short meaning) {
  if(wifi_client.connected()) {
    return;
  }
  if(!wifi_client.connect(ip, port)) {
    return;
  }
  unsigned char buff[12];
  buff[0] = t_id >> 8;
  buff[1] = t_id & 0xff;
  buff[2] = 0;
  buff[3] = 0;
  buff[4] = 0;
  buff[5] = 6;
  buff[6] = dev_id;
  buff[7] = 0x06;
  buff[8] = 0;
  buff[9] = 2;
  buff[10] = meaning >> 8;
  buff[11] = meaning & 0xff;
  
  wifi_client.write(buff, 12);
  
  if(wifi_client.available() > 0) {
    wifi_client.read(buff, 12);
  }
  t_id++;
  wifi_client.stop();
}



  
