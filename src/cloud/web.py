import os

from aiohttp import web

from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1


BROKER_URI = os.environ.get('MQTT_BROKER_URI', 'mqtt://localhost:1883')


routes = web.RouteTableDef()


@routes.get('/')
async def index(request):
    return web.Response(text="LightIR Cloud\n")


@routes.post('/{device_id}/power')
async def toggle_power(request):
    device_id = request.match_info['device_id']
    await request.app['messaging_client'].publish(
        f'devices/{device_id}/power',
        b''
    )
    return web.Response(status=204)


@routes.post('/{device_id}/brighten')
async def brighten(request):
    device_id = request.match_info['device_id']
    await request.app['messaging_client'].publish(
        f'devices/{device_id}/brighten',
        b''
    )
    return web.Response(status=204)


@routes.post('/{device_id}/dim')
async def dim(request):
    device_id = request.match_info['device_id']
    await request.app['messaging_client'].publish(
        f'devices/{device_id}/dim',
        b''
    )
    return web.Response(status=204)


supported_colors = {'red', 'green', 'blue', 'white'}


@routes.post('/{device_id}/set_color')
async def set_color(request):
    device_id = request.match_info['device_id']

    data = await request.post()
    color = data['color']
    if color not in supported_colors:
        return web.Response(text="Requested color is not implemented\n", status=501)

    await request.app['messaging_client'].publish(
        f'devices/{device_id}/set_color',
        color.encode('utf-8')
    )

    return web.Response(status=204)


@routes.get('/{device_id}/remote')
async def get_remote(request):
    return web.FileResponse(f'{os.path.dirname(os.path.realpath(__file__))}/remote.html')


async def app():
    messaging_client = MQTTClient()
    await messaging_client.connect(BROKER_URI)

    app = web.Application()
    app['messaging_client'] = messaging_client
    app.add_routes(routes)

    async def handle_shutdown(app):
        await messaging_client.disconnect()

    app.on_shutdown.append(handle_shutdown)

    return app


if __name__ == '__main__':
    web.run_app(app(), port=16712)
