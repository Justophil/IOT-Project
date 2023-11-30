#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN D8
#define RST_PIN D1

MFRC522 rfid(SS_PIN, RST_PIN);  // Instance of the class

MFRC522::MIFARE_Key key;

byte nuidPICC[4];

// const char* ssid = "TP-Link_2AD8";
// const char* password = "14730078";
// const char* mqtt_server = "192.168.0.144";

const char* ssid = "iPhone a Philip";
const char* password = "edpo1s0kp8ty1";
const char* mqtt_server = "172.20.10.3";

WiFiClient vanieriot;
PubSubClient client(vanieriot);

//PubSubClient client/(vanieriot);

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
  initializeRFID();
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  if(!client.loop())
    client.connect("vanieriot");

//  client.loop();

  value = analogRead(pResistor);
  String val = String(value);
  Serial.println(val);
  client.publish("LightIntensity", val.c_str());
  delay(1000);
  
//  client.loop();

  if (!rfid.PICC_IsNewCardPresent())
    return;
  // Verify if the NUID has been readed
  if (!rfid.PICC_ReadCardSerial())
    return;
  Serial.print(F("PICC type: "));
  MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
  Serial.println(rfid.PICC_GetTypeName(piccType));
  // Check is the PICC of Classic MIFARE type
  if (piccType != MFRC522::PICC_TYPE_MIFARE_MINI && piccType != MFRC522::PICC_TYPE_MIFARE_1K && piccType != MFRC522::PICC_TYPE_MIFARE_4K) {
    Serial.println(F("Your tag is not of type MIFARE Classic."));
    return;
  }
  if (rfid.uid.uidByte[0] != nuidPICC[0] || rfid.uid.uidByte[1] != nuidPICC[1] || rfid.uid.uidByte[2] != nuidPICC[2] || rfid.uid.uidByte[3] != nuidPICC[3]) {
    Serial.println(F("A new card has been detected."));
    // Store NUID into nuidPICC array
    for (byte i = 0; i < 4; i++) {
      nuidPICC[i] = rfid.uid.uidByte[i];
    }
    Serial.println(F("The NUID tag is:"));
    Serial.print(F("In hex: "));
    printHex(rfid.uid.uidByte, rfid.uid.size);
    Serial.println();
    Serial.print(F("In dec: "));
    printDec(rfid.uid.uidByte, rfid.uid.size);
    Serial.println();
  } else Serial.println(F("Card read previously."));

  String nuidStr = nuidToString(nuidPICC, sizeof(nuidPICC));
  Serial.print(F("nuidPICC as a string: "));
  Serial.println(nuidStr);
  nuidStr.toUpperCase();
  char nuidChar[nuidStr.length() + 1];
  nuidStr.toCharArray(nuidChar, sizeof(nuidChar));
  client.publish("RFID", nuidChar);

  // Halt PICC
  rfid.PICC_HaltA();
  // Stop encryption on PCD
  rfid.PCD_StopCrypto1();
  delay(1000);
}

void printHex(byte* buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}

/**
   Helper routine to dump a byte array as dec values to Serial.
*/
void printDec(byte* buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], DEC);
  }
}

void initializeRFID() {
  SPI.begin();      // Init SPI bus
  rfid.PCD_Init();  // Init MFRC522
  Serial.println();
  Serial.print(F("Reader :"));
  rfid.PCD_DumpVersionToSerial();
  for (byte i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;
  }
  Serial.println();
  Serial.println(F("This code scan the MIFARE Classic NUID."));
  Serial.print(F("Using the following key:"));
  printHex(key.keyByte, MFRC522::MF_KEY_SIZE);
}

String nuidToString(byte* nuid, byte nuidSize) {
  String nuidStr = "";
  for (byte i = 0; i < nuidSize; i++) {
    if (nuid[i] < 0x10) {
      nuidStr += "0";
    }
    nuidStr += String(nuid[i], HEX);
  }
  return nuidStr;
}
