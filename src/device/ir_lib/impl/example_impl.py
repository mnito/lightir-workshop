import collections


IR_BUFFER_SIZE = 8192
IR_BUFFER = collections.deque(maxlen=IR_BUFFER_SIZE)


class IRContext:
    def __init__(self, buffer, buffer_size):
        self.buffer = buffer
        self.buffer_size = buffer_size

    def __str__(self):
        if not self.buffer:
            return '{}'

        return str({
            'buffer': list(self.buffer),
            'buffer_len': len(self.buffer),
            'buffer_max_len': self.buffer_size
        })


def ir_init():
    return IRContext(IR_BUFFER, IR_BUFFER_SIZE)


def ir_begin(ir_ctx):
    ir_ctx.buffer.clear()


def ir_mark(ir_ctx, time):
    ir_ctx.buffer.append(time)


def ir_space(ir_ctx, time):
    ir_ctx.buffer.append(time)


def ir_end(ir_ctx):
    print(ir_ctx)


def ir_deinit(ir_ctx):
    ir_ctx.buffer = None
    ir_ctx.buffer_size = None
