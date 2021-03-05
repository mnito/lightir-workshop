from .impl import (
    ir_begin,
    ir_mark,
    ir_space,
    ir_end
)


def ir_send_nec(ir_ctx, data, length=32):
    ir_begin(ir_ctx)

    ir_mark(ir_ctx, 9000)
    ir_space(ir_ctx, 4500)

    mask = 1 << length - 1

    while(mask):
        ir_mark(ir_ctx, 560)

        if data & mask:
            ir_space(ir_ctx, 1690)
        else:
            ir_space(ir_ctx, 560)

        mask >>= 1

    ir_mark(ir_ctx, 560)
    ir_space(ir_ctx, 0)

    ir_end(ir_ctx)
