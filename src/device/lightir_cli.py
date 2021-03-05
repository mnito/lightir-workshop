import readline

import lightir_codes
from ir_lib import ir_init, ir_deinit, ir_send_nec

commands = {
    'power': lightir_codes.POWER,
    'red': lightir_codes.RED,
    'green': lightir_codes.GREEN,
    'blue': lightir_codes.BLUE,
    'brighten': lightir_codes.BRIGHTEN,
    'dim': lightir_codes.DIM
}

ir_ctx = ir_init()

while True:
    command = input('Enter a command: ')

    if command.endswith('exit'):
        break

    if command in commands:
        ir_send_nec(ir_ctx, commands[command])
        print('Sending {}'.format(hex(commands[command])))
    else:
        print('Command unavailable.')


ir_deinit(ir_ctx)
