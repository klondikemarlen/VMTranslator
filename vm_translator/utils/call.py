from vm_translator.utils.basic import PUSH_D_STACK, SET_D


class Call:
    PUSH_RETURN_ADDR = '\n'.join([
        "@RETURN{call_count}",  # same as 'return-label'
        "D=A",
        PUSH_D_STACK,
    ])

    PUSH_VAR_ADDR = "\n".join([  # push LCL, ARG, THIS or THAT
        "@{}",
        "D=M",
        PUSH_D_STACK
    ])

    REPOSITION_ARG = '\n'.join([  # ARG = SP-n-5
        SET_D,  # D = n
        "@5",
        "D=D+A",  # D = n+5
        "@SP",
        "D=M-D",  # SP-n-5 == SP-(n+5)
        "@ARG",
        "M=D",
    ])

    REPOSITION_LCL = '\n'.join([  # LCL = SP
        "@SP",
        "D=M",
        "@LCL",
        "M=D"
    ])

    TRANSFER_CONTROL = '\n'.join([
        "@{func}",
        "0;JMP"
    ])

    LABEL_RETURN_ADDR = "\n".join([
        "(RETURN{call_count})"
    ])

    CALL = '\n'.join([
        PUSH_RETURN_ADDR,
        PUSH_VAR_ADDR.format("LCL"),
        PUSH_VAR_ADDR.format("ARG"),
        PUSH_VAR_ADDR.format("THIS"),
        PUSH_VAR_ADDR.format("THAT"),
        REPOSITION_ARG,
        REPOSITION_LCL,
        TRANSFER_CONTROL,
        LABEL_RETURN_ADDR
    ]).split()
