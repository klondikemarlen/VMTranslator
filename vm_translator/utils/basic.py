INC_STACK_ADDR = "\n".join([
    "@SP",
    "M=M+1"
])

POP_STACK_ADDR_A = "\n".join([
    "@SP",
    "AM=M-1",
])

POP_STACK_D = "\n".join([
    POP_STACK_ADDR_A,
    "D=M"
])

STACK_ADDR = "\n".join([
    "@SP",
    "A=M"
])

STACK_OVERWRITE = '\n'.join([
    "@SP",
    "A=M-1",  # Simulate stack pop followed by pushing result
    # stack address remains the same and gets overwritten.
])

STACK_ADDR_A_INC = '\n'.join([
    "@SP",
    "M=M+1",  # increment stack address
    "A=M-1",  # set A original stack address
])

PUSH_D_STACK = '\n'.join([
    STACK_ADDR_A_INC,
    "M=D",  # set previous address to D.
])

SET_D = "\n".join([
    "@{const}",
    "D=A"
])
