#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// const char* ssid = "TP-Link_2AD8";
// const char* password = "14730078";
// const char* mqtt_server = "192.168.0.144";

const char* ssid = "iPhone a Philip";
const char* password = "edpo1s0kp8ty1";
const char* mqtt_server = "172.20.10.3";

WiFiClient vanieriot;
PubSubClient client(vanieriot);

const int pResistor = A0;
const int led = D0;
int value;

void setup_wifi() {
   delay(10);
   Serial.println();
   Serial.print("Connecting to ");
   Serial.println(ssid);
   WiFi.begin(ssid, password);
   while (WiFi.status() != WL_CONNECTED) {
     delay(500);
     Serial.print(".");
   }
   Serial.println("");
   Serial.print("WiFi connected - ESP-8266 IP address: ");
   Serial.println(WiFi.localIP());
}
void callback(String topic, byte* message, unsigned int length) {
   Serial.print("Message arrived on topic: ");
   Serial.print(topic);
   Serial.print(". Message: ");
   String messagein;
   for (int i = 0; i < length; i++) {
     Serial.print((char)message[i]);
     messagein += (char)message[i];
   }
}

void reconnect() {
   while (!client.connected()) {
     Serial.print("Attempting MQTT connection...");
     if (client.connect("vanieriot")) {
       Serial.println("connected");
     }
     else {
       Serial.print("failed, rc=");
       Serial.print(client.state());
       Serial.println(" try again in 3 seconds");
       delay(3000);
     }
   }
}
void setup() {
  Serial.begin(115200);
  pinMode(pResistor, INPUT);
  pinMode(led,OUTPUT);
  digitalWrite(led, LOW);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  if(!client.loop())
    client.connect("vanieriot");
  int value = analogRead(pResistor);
  if(value < 400) {
    digitalWrite(led, HIGH);
  }
  else {
    digitalWrite(led, LOW);
  }
  String val = String(value);
  Serial.println(value);
  Serial.println(val);
  client.publish("LightIntensity", val.c_str());
  delay(1000);
}
