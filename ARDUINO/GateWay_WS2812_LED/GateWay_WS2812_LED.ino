#include <FastLED.h>

#define LED_PIN     3
#define NUM_LEDS    24
CRGB leds[NUM_LEDS];
int loading = 0;
////////--------------------------------
#include <RF24.h>
#include <RF24Network.h>
#include <SPI.h>
//////--------------------------------------
RF24 radio(7, 8); // CNS, CE
RF24Network network(radio); 
const uint16_t this_node = 00; 

uint8_t received_data[10]; //Number of channels
uint8_t num_received_data = sizeof(received_data);//*********
//
bool node_1 = false;
bool node_2 = false;

char inByte = '0';

int list[10];

void setup() {
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);

  Serial.begin(9600);  
  Display_promini(0);

  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  
  establishContact();
  SPI.begin();
  radio.begin();
  network.begin(90, this_node); //(channel, node address)   
}

void loop() {
  network.update();
  if (Serial.available() > 0){
    inByte = Serial.read();
    if(inByte == 's'){sent_data();}
    if(inByte == 'n'){get_it();}
    if(inByte == 'w'){setColor(100, 100, 100);}
    if(inByte == 'g'){setColor(0, 255, 0);}
    if(inByte == 'y'){setColor(190, 120, 0);}
    if(inByte == 'o'){setColor(255, 50, 0);}
    if(inByte == 'r'){setColor(255, 0, 0);}
    if(inByte == 'm'){setColor(255, 0, 100);}
    if(inByte == 'l'){loadingLight();}
  }
  get_data();
  delay(10);
 }

void get_it()
  {
  int num_of_nodes = int(node_1)+int(node_2);
  Serial.println(num_of_nodes);
  }

void sent_data(){
  for(int i = 0; i< num_received_data; i++)
    {
      Serial.print(received_data[i]);
      Serial.print('-');
      }
    Serial.println();
  }

void get_data(){  
   uint8_t incomingData[5];
   bool ok;
   int val;
   RF24NetworkHeader header;
   while ( network.available() ) {     // Is there any incoming data?
     ok = network.read(header, &incomingData, sizeof(incomingData));
     val = header.from_node;
   }
   
   for (int i=0; i<10; i++) {
    if (i == 9)list[i] = val;
    else list[i] = list[i+1];
   }
   
   int sum= 0;
   for (int i=0; i<10; i++){sum+= list[i];}
   if (sum == 10){node_1 = true;node_2 = false;}
   else if (sum == 20){node_1 = false;node_2 = true;}
   else if (sum < 10){node_1 = false; node_2 = false;}
   else {node_1 = true; node_2 = true;}
   
   if (val == 1){
    for( int i = 0; i < 5; i++)
    received_data[i] = incomingData[i];
   }
   else if(val == 2){
    for( int i = 5; i < 10; i++)
    received_data[i] = incomingData[i-5];
   }
 }

void establishContact() {
  while (Serial.available() <= 0) {
    Serial.println("A");   // send an initial string
    Display_promini(0);
    delay(300);
  }
  Serial.flush();
}

void setColor(int red, int green, int blue)
{
    for (int i = 15; i >= 0; i--) {
    leds[i] = CRGB ( red, green, blue);
    FastLED.show();
    delay(40);
    }
}

void loadingLight(){
  loading = loading + 1;
  if(loading <5) {leds[loading] = CRGB ( 0, 0, 255);}
  else if(loading <10) {leds[loading] = CRGB ( 0, 255, 0);}
  else {leds[loading] = CRGB ( 255, 0, 0);}  
  FastLED.show();
}
