from .basic import (
    STACK_ADDR,
    POP_STACK_D,
    POP_STACK_ADDR_A,
    INC_STACK_ADDR,
    STACK_OVERWRITE
)


class ArithmeticCode:
    ADD = "\n".join([
        POP_STACK_D,
        STACK_OVERWRITE,  # simulate pop from stack then pus result
        "M=M+D",
    ])

    SUB = "\n".join([  # a - b = m
        POP_STACK_D,  # b
        STACK_OVERWRITE,  # a
        "M=M-D",  # a - b = m
    ])

    NEG = "\n".join([
        STACK_OVERWRITE,
        "M=-M",
    ])

    NOT = "\n".join([
        STACK_OVERWRITE,
        "M=!M",
    ])

    AND = "\n".join([
        POP_STACK_D,
        STACK_OVERWRITE,
        "M=M&D",
    ])

    OR = "\n".join([
        POP_STACK_D,
        STACK_OVERWRITE,
        "M=M|D",
    ])

    IF_TRUE_ADDR = "@IFTRUE{}"
    PUSH_IF_TRUE_STACK = "\n".join([
        STACK_ADDR,
        "M=0",  # if a != b, m = 0, false
        "@ENDIF{}",
        "0;JMP",
        "(IFTRUE{})",
        STACK_ADDR,
        "M=-1",  # if a == b, m = -1 (1111111111111111), true
        "(ENDIF{})"
    ])

    EQ = "\n".join([  # a == b
        POP_STACK_D,  # b
        POP_STACK_ADDR_A,  # a
        "D=M-D",  # a - b = d, d used for comparison, subtraction
        IF_TRUE_ADDR,
        "D;JEQ",  # D used for comparison
        PUSH_IF_TRUE_STACK,
        INC_STACK_ADDR
    ])

    GT = "\n".join([  # if a > b, m = -1 otherwise m = 0
        POP_STACK_D,  # b
        POP_STACK_ADDR_A,  # a
        "D=M-D",  # a - b = d, d used for comparison
        IF_TRUE_ADDR,
        "D;JGT",  # a - b > 0 if a > b
        PUSH_IF_TRUE_STACK,
        INC_STACK_ADDR
    ])

    LT = "\n".join([
        POP_STACK_D,
        POP_STACK_ADDR_A,
        "D=M-D",
        IF_TRUE_ADDR,
        "D;JLT",
        PUSH_IF_TRUE_STACK,
        INC_STACK_ADDR
    ])

    CONVERSION = {
        'add': ADD.split(),
        'sub': SUB.split(),
        'neg': NEG.split(),
        'eq': EQ.split(),
        'gt': GT.split(),
        'lt': LT.split(),
        "and": AND.split(),
        "or": OR.split(),
        "not": NOT.split()
    }
