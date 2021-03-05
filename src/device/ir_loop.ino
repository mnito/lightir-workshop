#include "IRremote.h"

#define IR_BUFFER_SIZE 512
#define IR_CARRIER_FREQUENCY 38

IRsend irSender;

unsigned int irBuffer[IR_BUFFER_SIZE];
size_t irBufferPos = 0;

void setup() {
    Serial.begin(9600);
}

void loop() {
    if (!Serial.available()) {
        return;
    }

    byte incomingBytes[4];
    Serial.readBytes(incomingBytes, 4);
    irBuffer[irBufferPos] = (
        (unsigned int) incomingBytes[0]
        | (unsigned int) incomingBytes[1] << 8
    );

    if (irBuffer[irBufferPos]) {
        irBufferPos++;
        return;
    }

    irSender.sendRaw(irBuffer, irBufferPos + 1, IR_CARRIER_FREQUENCY);
    irBufferPos = 0;
    Serial.write(1);
}
