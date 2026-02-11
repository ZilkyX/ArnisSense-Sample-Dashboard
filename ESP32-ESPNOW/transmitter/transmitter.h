#pragma once
#include <Arduino.h>
#include <WiFi.h>
#include <esp_now.h>

typedef struct __attribute__((packed)) {
    uint8_t  playerID;
    uint8_t  nodeID;
    uint16_t peak;
    uint16_t duration;
    uint32_t time;
    uint16_t seq;
} StrikePacket;

class Transmitter {
public:
    Transmitter(uint8_t playerID,
                uint8_t nodeID,
                const uint8_t receiverMAC[6],
                uint8_t buttonPin);

    void begin();
    void loop();   

private:
    uint8_t playerID;
    uint8_t nodeID;
    uint8_t buttonPin;
    uint8_t receiverMAC[6];

    uint16_t seq = 0;
    bool buttonPressed = false;

    static void onDataSent(const uint8_t *mac_addr,
                           esp_now_send_status_t status);

    void sendStrike();
};
