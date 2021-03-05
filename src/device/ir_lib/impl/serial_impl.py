import collections
import time

import serial


class IRContext:
    def __init__(self, fd):
        self.fd = fd


def ir_init():
    # fd = serial.Serial('/dev/ttyACM0', 9600, timeout=2)
    fd = serial.Serial('/dev/tty.usbmodem14201', 9600, timeout=2)
    return IRContext(fd)


def ir_begin(ir_ctx):
    pass


def ir_mark(ir_ctx, time):
    ir_ctx.fd.write(time.to_bytes(4, byteorder='little'))


def ir_space(ir_ctx, time):
    ir_ctx.fd.write(time.to_bytes(4, byteorder='little'))


def ir_end(ir_ctx):
    pass


def ir_deinit(ir_ctx):
    ir_ctx.fd.close()
