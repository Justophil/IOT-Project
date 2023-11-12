#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// const char* ssid = "TP-Link_2AD8";
// const char* password = "14730078";
// const char* mqtt_server = "192.168.0.144";

const char* ssid = "TP-Link_2AD8";
const char* password = "14730078";
const char* mqtt_server = "192.168.0.144";

WiFiClient vanieriot;
PubSubClient client(vanieriot);

const int pResistor = A0;
const int led = 2;
int value;

void setup_wifi() {
   delay(10);
   // We start by connecting to a WiFi network
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
       // Wait 3 seconds before retrying
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
  String val = str(value);
  client.publish("LightIntensity", val.c_str());
  delay(1000);
}
