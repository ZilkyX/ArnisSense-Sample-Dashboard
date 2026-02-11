#include "Receiver.h"

Receiver receiver;

void setup() {
    receiver.begin();

    receiver.setCallback([](const StrikePacket& pkt) {
    });
}

void loop() {
}
