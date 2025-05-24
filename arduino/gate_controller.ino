const int gateEntryRelay = 7;
const int gateExitRelay = 8;

void setup() {
  pinMode(gateEntryRelay, OUTPUT);
  pinMode(gateExitRelay, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    if (cmd == "OPEN_ENTRY") {
      digitalWrite(gateEntryRelay, HIGH);
      delay(1000); // Hold relay for 1s
      digitalWrite(gateEntryRelay, LOW);
      Serial.println("ENTRY_OPENED");
    } else if (cmd == "OPEN_EXIT") {
      digitalWrite(gateExitRelay, HIGH);
      delay(1000);
      digitalWrite(gateExitRelay, LOW);
      Serial.println("EXIT_OPENED");
    }
  }
}