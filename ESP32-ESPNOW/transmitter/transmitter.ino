#include "Transmitter.h"

uint8_t receiverMAC[6] = {0x68, 0xFE, 0x71, 0x0D, 0x81, 0x34};

Transmitter tx(2, 2, receiverMAC, 25);

void setup() {
    tx.begin();
}

void loop() {
    tx.loop();
}
