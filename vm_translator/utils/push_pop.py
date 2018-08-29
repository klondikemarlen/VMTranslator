from .basic import POP_STACK_D
from vm_translator.utils.basic import PUSH_D_STACK, SET_D


class PushPopCodes:
    COMPUTE_SEGMENT_ADDR = "\n".join([  # store address of 'local[x]' in R13
        SET_D,  # start computing local[x]
        "@{seg}",  # could be optimized if computing local 0
        "D=D+M",
        "@R13",  # use extra virtual register, located at RAM[13]
        "M=D"  # R13 now holds the address of local[x]
    ])

    POP_SEGMENT_COMPUTE_ADDR = "\n".join([
        COMPUTE_SEGMENT_ADDR,
        POP_STACK_D,
        "@R13",
        "A=M",
        "M=D"
    ])

    PUSH_SEGMENT_COMPUTE_ADDR = '\n'.join([
        SET_D,
        "@{seg}",
        "A=D+M",
        "D=M",  # fetch object from segment ..
        PUSH_D_STACK
    ])

    PUSH_CONSTANT = "\n".join([
        SET_D,
        PUSH_D_STACK
    ])

    PUSH_GLOBAL = '\n'.join([
        "@{seg}",
        "D=M",
        PUSH_D_STACK,
    ])

    POP_GLOBAL = '\n'.join([
        POP_STACK_D,
        "@{seg}",
        "M=D",
    ])

    PUSH_SEGMENT_CONVERSION = {
        'local': ("LCL", PUSH_SEGMENT_COMPUTE_ADDR.split()),
        'argument': ("ARG", PUSH_SEGMENT_COMPUTE_ADDR.split()),
        'this': ("THIS", PUSH_SEGMENT_COMPUTE_ADDR.split()),
        'that': ("THAT", PUSH_SEGMENT_COMPUTE_ADDR.split()),
        'constant': (None, PUSH_CONSTANT.split()),
        'temp': (None, PUSH_GLOBAL.split()),
        'static': (None, PUSH_GLOBAL.split()),
        'pointer': (None, PUSH_GLOBAL.split()),
    }

    POP_SEGMENT_CONVERSION = {
        'local': ("LCL", POP_SEGMENT_COMPUTE_ADDR.split()),
        'argument': ("ARG", POP_SEGMENT_COMPUTE_ADDR.split()),
        'this': ("THIS", POP_SEGMENT_COMPUTE_ADDR.split()),
        'that': ("THAT", POP_SEGMENT_COMPUTE_ADDR.split()),
        'temp': (None, POP_GLOBAL.split()),
        'static': (None, POP_GLOBAL.split()),
        'pointer': (None, POP_GLOBAL.split())
    }

    CONVERSION = {
        'push': PUSH_SEGMENT_CONVERSION,
        'pop': POP_SEGMENT_CONVERSION
    }
