/*
 * Arduino slave code for Rubik's Cube Solver project
 * 
 * Code is responsible for taking in commands from Pi via serial input from USB cable and using this info to control
 * the 6 Neo Pixel ring lights that illuminate the cube
 */

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

// Number of pixels on each ring - change for different hardware
#define NUMPIXELS 16 

// Pins on Arduino being used - change here if pins change
int pins[6] = {2,3,4,5,6,7};

Adafruit_NeoPixel pixels_1(NUMPIXELS, pins[0], NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixels_2(NUMPIXELS, pins[1], NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixels_3(NUMPIXELS, pins[2], NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixels_4(NUMPIXELS, pins[3], NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixels_5(NUMPIXELS, pins[4], NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixels_6(NUMPIXELS, pins[5], NEO_GRB + NEO_KHZ800);

#define DELAYVAL 5000 // Time (in milliseconds) to pause between pixels

void setup() {
  // begin serial connection
  Serial.begin(9600);

  // Initialization of the 6 Neo Pixel rings
  // bottom camera lights
  pixels_1.begin(); 
  pixels_2.begin();
  pixels_3.begin();

  // top camera lights
  pixels_4.begin();
  pixels_5.begin();
  pixels_6.begin();
}

void loop() {
  // detects incoming serial input
  if (Serial.available() > 0) {
    int command = Serial.read();
    
    if (command == 'B') {
      light_bottom(255,255,255);
      Serial.print("bottom lit!");
      Serial.write("\n");
    } else if (command == 'T') {
      light_top(255,255,255);
      Serial.print("top lit!");
      Serial.write("\n");
    } else if (command == 'D') {
      brightness(1);
      Serial.print("brightness: low");
      Serial.write("\n");
    } else if (command == 'L') {
      brightness(255);
      Serial.print("brightness: high");
      Serial.write("\n");
    } else if (command == 'X') {
      clear_bottom();
      Serial.print("bottom cleared");
      Serial.write("\n");
    } else if (command == 'Y') {
      clear_top();
      Serial.print("top cleared");
      Serial.write("\n");
    } else if (command == 'Z') {
      clear_all();
      Serial.print("all cleared");
      Serial.write("\n");
    } else if (command == 'M') {
      light_top(0,0,255);
      Serial.print("top lit blue!");
      Serial.write("\n");
    } else if (command == 'N') {
      light_bottom(0,0,255);
      Serial.print("bottom lit blue!");
      Serial.print("\n");
    }
  }
}

// sets the brightness of all lights to the input value
void brightness(int i) {
   pixels_1.setBrightness(i);
   pixels_2.setBrightness(i);
   pixels_3.setBrightness(i);
   pixels_4.setBrightness(i);
   pixels_5.setBrightness(i);
   pixels_6.setBrightness(i);
   
   pixels_1.show();   
   pixels_2.show();   
   pixels_3.show();
   pixels_4.show();   
   pixels_5.show();   
   pixels_6.show();
}

// lights the bottom rings
void light_bottom(int r, int g, int b) {
  for(int i=0; i<NUMPIXELS; i++) {
    // sets all light colors to white
    pixels_1.setPixelColor(i, pixels_1.Color(r, g, b));
    pixels_2.setPixelColor(i, pixels_2.Color(r, g, b));
    pixels_3.setPixelColor(i, pixels_3.Color(r, g, b));
  }

  pixels_1.show();   
  pixels_2.show();   
  pixels_3.show();
}

// lights the top rings
void light_top(int r, int g, int b) {
  for(int i=0; i<NUMPIXELS; i++) {
    // sets all light colors to white
    pixels_4.setPixelColor(i, pixels_1.Color(r, g, b));
    pixels_5.setPixelColor(i, pixels_2.Color(r, g, b));
    pixels_6.setPixelColor(i, pixels_3.Color(r, g, b));
  }

  pixels_4.show();   
  pixels_5.show();   
  pixels_6.show();
}

// clears all lights for the bottom camera
void clear_bottom() {
  pixels_1.clear(); 
  pixels_2.clear();
  pixels_3.clear();

  pixels_1.show();   
  pixels_2.show();   
  pixels_3.show();
}


void clear_top() {
  pixels_4.clear(); 
  pixels_5.clear();
  pixels_6.clear();

  pixels_4.show();   
  pixels_5.show();   
  pixels_6.show();
}

// Set all pixel colors to 'off'
void clear_all() {
  // set all pixels to have no color
  pixels_1.clear(); 
  pixels_2.clear();
  pixels_3.clear();
  pixels_4.clear();
  pixels_5.clear();
  pixels_6.clear();

  pixels_1.show();   
  pixels_2.show();   
  pixels_3.show();
  pixels_4.show();   
  pixels_5.show();   
  pixels_6.show();
}
