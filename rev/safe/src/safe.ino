const byte rowPins[4] = { 9, 8, 7, 6 };
const byte colPins[4] = { 5, 4, 3, 2 };
// bctf{B5D2A160B062538BC55D}
byte buf[20] = {};
const byte password[20] = {
  13, 5, 15,
   4, 12, 0,
   9, 7, 13,
   7, 9, 4,
   5, 8, 6,
  13, 14, 5,
   5, 15};
byte i = 0;

#define RELAY 10
#define LED 11

void setup() {
  // put your setup code here, to run once:
  pinMode(RELAY, OUTPUT);
  pinMode(LED, OUTPUT);

  for (byte i = 0; i < 4; i++) {
    pinMode(rowPins[i], INPUT_PULLUP);
    pinMode(colPins[i], OUTPUT);
    digitalWrite(colPins[i], HIGH);
  }
}

void loop() {
  for (byte c = 0; c < 4; c++) {
    digitalWrite(colPins[c], LOW);
    for (byte r = 0; r < 4; r++) {
      if (!digitalRead(rowPins[r])) {
        while (!digitalRead(rowPins[r])) {
        }
        buf[i] = 4 * c + r;
        i++;
        delay(50);
      }
    }
    digitalWrite(colPins[c], HIGH);
  }
  if (i == 20) {
    for (byte j = 0; j < 20; j++) {
      if (buf[j] != password[j]) {
        for (byte n = 0; n < 5; n++) {
          digitalWrite(LED, 1);
          delay(500);
          digitalWrite(LED, 0);
          delay(500);
        }
        i = 0;
        memset(buf, 0, sizeof(buf));
        return;
      }
    }
    
    digitalWrite(RELAY, 1);
    delay(10000);
    digitalWrite(RELAY, 0);
    
    i = 0;
    memset(buf, 0, sizeof(buf));
  }
}
