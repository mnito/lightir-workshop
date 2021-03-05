import asyncio
import json
import os

from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1

import lightir_codes
import ir_lib


BROKER_URI = os.environ.get('MQTT_BROKER_URI', 'mqtt://localhost:1883')

DEVICE_IDENTIFIER = 'LIGHTIR_DEV'
DEVICE_TOPIC = f'/devices/{DEVICE_IDENTIFIER}/+'


def toggle_power(ir_ctx, payload=None):
    ir_lib.ir_send_nec(ir_ctx, lightir_codes.POWER)

def brighten(ir_ctx, payload=None):
    ir_lib.ir_send_nec(ir_ctx, lightir_codes.BRIGHTEN)

def dim(ir_ctx, payload=None):
    ir_lib.ir_send_nec(ir_ctx, lightir_codes.DIM)


color_to_lightir_code = {
    'red': lightir_codes.RED,
    'green': lightir_codes.GREEN,
    'blue': lightir_codes.BLUE,
    'white': lightir_codes.WHITE,
}


def set_color(ir_ctx, payload):
    color = payload.decode('utf-8')
    if color not in color_to_lightir_code:
        raise NotImplementedError("Color not handled")

    ir_lib.ir_send_nec(ir_ctx, color_to_lightir_code[color])


handlers = {
    f'devices/{DEVICE_IDENTIFIER}/power': toggle_power,
    f'devices/{DEVICE_IDENTIFIER}/brighten': brighten,
    f'devices/{DEVICE_IDENTIFIER}/dim': dim,
    f'devices/{DEVICE_IDENTIFIER}/set_color': set_color,
}


async def listen():
    IR_CTX = ir_lib.ir_init()

    client = MQTTClient()
    await client.connect(BROKER_URI)
    await client.subscribe([(f'devices/{DEVICE_IDENTIFIER}/+', QOS_1)])
    while True:
        message = await client.deliver_message()
        topic = message.publish_packet.variable_header.topic_name
        payload = message.publish_packet.payload.data
        if topic not in handlers:
            print(f"unhandled topic {topic}: skipping")
            continue

        handlers[topic](IR_CTX, payload)
        print(f"handled message to {topic} with payload '{payload.decode('utf-8')}'")

    await client.unsubscribe([f'devices/{DEVICE_IDENTIFIER}/+'])
    await client.disconnect()

    ir_lib.ir_deinit(app['ir_ctx'])


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(listen())
