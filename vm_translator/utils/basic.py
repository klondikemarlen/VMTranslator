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
    INC_STACK_ADDR,  # move stack forward by 1.
    "A=M-1",  # get address of previous stack.
    "M=D",  # set previous address to D.
])

SET_D = "\n".join([
    "@{const}",
    "D=A"
])
