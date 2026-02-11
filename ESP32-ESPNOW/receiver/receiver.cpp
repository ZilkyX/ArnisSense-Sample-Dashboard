#include "Receiver.h"

Receiver* Receiver::instance = nullptr;

Receiver::Receiver() {
    instance = this;
}

void Receiver::begin() {
    Serial.begin(115200);
    delay(200);

    WiFi.mode(WIFI_STA);
    WiFi.setSleep(false);

    if (esp_now_init() != ESP_OK) {
        return;
    }

    esp_now_register_recv_cb(onDataRecvStatic);

}

void Receiver::setCallback(void (*cb)(const StrikePacket& pkt)) {
    userCallback = cb;
}

void Receiver::onDataRecvStatic(const esp_now_recv_info *info,
                                const uint8_t *data,
                                int len) {
    if (instance) {
        instance->handleData(data, len);
    }
}

void Receiver::handleData(const uint8_t *data, int len) {
    if (len != sizeof(StrikePacket)) return;

    const StrikePacket* pkt =
        reinterpret_cast<const StrikePacket*>(data);

    uint8_t player = pkt->playerID;
    uint8_t node   = pkt->nodeID;

    if (player < 1 || player > 2) return;
    if (node >= MAX_NODES) return;

    uint16_t &last = lastSeq[player][node];
    if (pkt->seq <= last) return;
    last = pkt->seq;

    Serial.printf(
            "{\"player\":%d,"
            "\"node\":%d,"
            "\"peak\":%d,"
            "\"duration\":%d,"
            "\"time\":%lu,"
            "\"seq\":%d}\n",
            pkt->playerID,
            pkt->nodeID,
            pkt->peak,
            pkt->duration,
            pkt->time,
            pkt->seq
        );

    if (userCallback) {
        userCallback(*pkt);
    }
}
