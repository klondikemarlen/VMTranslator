INC_STACK_ADDR = "\n".join([
    "@SP",
    "M=M+1"
])

POP_STACK_ADDR = "\n".join([
    "@SP",
    "M=M-1",
    "A=M"
])

POP_STACK_D = "\n".join([
    POP_STACK_ADDR,
    "D=M"
])

STACK_ADDR = "\n".join([
    "@SP",
    "A=M"
])

PUSH_D_STACK = '\n'.join([
    STACK_ADDR,
    "M=D",
    INC_STACK_ADDR
])

SET_D = "\n".join([
    "@{const}",
    "D=A"
])
