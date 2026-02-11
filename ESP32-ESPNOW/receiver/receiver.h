#pragma once
#include <Arduino.h>
#include <WiFi.h>
#include <esp_now.h>

#define MAX_NODES 10

typedef struct __attribute__((packed)) {
    uint8_t  playerID;   
    uint8_t  nodeID;     
    uint16_t peak;       
    uint16_t duration;   
    uint32_t time;       
    uint16_t seq;        
} StrikePacket;

class Receiver {
public:
    Receiver();
    void begin();
    void setCallback(void (*cb)(const StrikePacket& pkt));

private:
    static Receiver* instance;

    uint16_t lastSeq[3][MAX_NODES] = {0};

    void (*userCallback)(const StrikePacket& pkt) = nullptr;

    static void onDataRecvStatic(const esp_now_recv_info *info,
                                 const uint8_t *data,
                                 int len);

    void handleData(const uint8_t *data, int len);
};
