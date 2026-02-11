#include "Transmitter.h"

Transmitter::Transmitter(uint8_t pID,
                         uint8_t nID,
                         const uint8_t rMAC[6],
                         uint8_t btnPin) {
    playerID  = pID;
    nodeID    = nID;
    buttonPin = btnPin;
    memcpy(receiverMAC, rMAC, 6);
}

void Transmitter::begin() {
    Serial.begin(115200);
    delay(200);

    pinMode(buttonPin, INPUT_PULLUP);

    WiFi.mode(WIFI_STA);
    WiFi.setSleep(false);

    if (esp_now_init() != ESP_OK) {
        Serial.println("ESP-NOW init failed");
        return;
    }

    esp_now_register_send_cb(onDataSent);

    esp_now_peer_info_t peerInfo = {};
    memcpy(peerInfo.peer_addr, receiverMAC, 6);
    peerInfo.channel = 0;
    peerInfo.encrypt = false;

    if (esp_now_add_peer(&peerInfo) != ESP_OK) {
        Serial.println("Failed to add peer");
        return;
    }

    Serial.println("Transmitter ready");
}

void Transmitter::loop() {
    bool state = digitalRead(buttonPin);

    if (state == LOW && !buttonPressed) {
        buttonPressed = true;
        sendStrike();
    }

    if (state == HIGH) {
        buttonPressed = false;
    }
}

void Transmitter::sendStrike() {
    StrikePacket pkt;
    pkt.playerID = playerID;
    pkt.nodeID   = nodeID;
    pkt.peak     = 900;
    pkt.duration = 40;
    pkt.time     = millis();
    pkt.seq      = ++seq;

    esp_err_t result = esp_now_send(receiverMAC,
                                    (uint8_t*)&pkt,
                                    sizeof(pkt));

    if (result == ESP_OK) {
        Serial.println("Strike sent!");
    } else {
        Serial.println("Send failed");
    }
}

void Transmitter::onDataSent(const uint8_t *mac_addr,
                             esp_now_send_status_t status) {
    Serial.print("Send status: ");
    Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Success" : "Fail");
}
