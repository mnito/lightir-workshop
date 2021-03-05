from aiohttp import web

import lightir_codes
import ir_lib


routes = web.RouteTableDef()


@routes.get('/')
async def index(request):
    return web.Response(text="LightIR\n")


@routes.post('/power')
async def toggle_power(request):
    ir_lib.ir_send_nec(request.app['ir_ctx'], lightir_codes.POWER)

    return web.Response(status=204)


@routes.post('/brighten')
async def brighten(request):
    ir_lib.ir_send_nec(request.app['ir_ctx'], lightir_codes.BRIGHTEN)

    return web.Response(status=204)


@routes.post('/dim')
async def dim(request):
    ir_lib.ir_send_nec(request.app['ir_ctx'], lightir_codes.DIM)

    return web.Response(status=204)


color_to_lightir_code = {
    'red': lightir_codes.RED,
    'green': lightir_codes.GREEN,
    'blue': lightir_codes.BLUE,
    'white': lightir_codes.WHITE,
}


@routes.post('/color')
async def set_color(request):
    data = await request.post()
    color = data['color']
    if color not in color_to_lightir_code:
        return web.Response(text="Requested color is not implemented\n", status=501)

    ir_lib.ir_send_nec(request.app['ir_ctx'], color_to_lightir_code[color])

    return web.Response(status=204)


@routes.get('/remote')
async def get_remote(request):
    return web.FileResponse('./remote.html')


async def app():
    ir_ctx = ir_lib.ir_init()

    app = web.Application()
    app['ir_ctx'] = ir_ctx
    app.add_routes(routes)

    async def handle_shutdown(app):
        ir_lib.ir_deinit(app['ir_ctx'])

    app.on_shutdown.append(handle_shutdown)

    return app


if __name__ == '__main__':
    web.run_app(app(), port=16712)
