import collections
import time

import serial


IR_BUFFER_SIZE = 1024
IR_BUFFER = collections.deque(maxlen=IR_BUFFER_SIZE)


class IRContext:
    def __init__(self, buffer, buffer_size, fd):
        self.buffer = buffer
        self.buffer_size = buffer_size
        self.fd = fd

    def __str__(self):
        if not self.buffer:
            return '{}'

        return str({
            'buffer': list(self.buffer),
            'buffer_len': len(self.buffer),
            'buffer_max_len': self.buffer_size,
            'fd': self.fd
        })


def ir_init():
    fd = serial.Serial('/dev/ttyACM0', 9600, timeout=2)
    return IRContext(IR_BUFFER, IR_BUFFER_SIZE, fd)


def ir_begin(ir_ctx):
    ir_ctx.buffer.clear()


def ir_mark(ir_ctx, time):
    ir_ctx.buffer.extend(time.to_bytes(4, byteorder='little'))


def ir_space(ir_ctx, time):
    ir_ctx.buffer.extend(time.to_bytes(4, byteorder='little'))


def ir_end(ir_ctx):
    buffer_bytes = bytes(ir_ctx.buffer)
    ir_ctx.fd.write(buffer_bytes)


def ir_deinit(ir_ctx):
    ir_ctx.fd.close()
    ir_ctx.fd = None
    ir_ctx.buffer = None
    ir_ctx.buffer_size = None
