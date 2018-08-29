from .basic import INC_STACK_ADDR, POP_STACK_D
from vm_translator.utils.basic import STACK_ADDR


class FunctionReturn:
    PUSH_0 = '\n'.join([
        STACK_ADDR,
        "M=0",
        INC_STACK_ADDR
    ])

    @staticmethod
    def setup_n_local(n):
        return '\n'.join([FunctionReturn.PUSH_0] * n).split()

    SAVE_LOCAL_R13 = "\n".join([
        "@LCL",
        "D=M",
        "@R13",
        "M=D",  # lcl/frame stored at temp.reg.1/R13
    ])

    SAVE_RETURN_ADDR_R14 = '\n'.join([
        # "@R13",
        # "D=M",  # if I choose not to reuse D
        "@5",
        "A=D-A",  # reusing D (lcl/frame) from previous equation.
        "D=M",
        "@R14",
        "M=D"  # return address stored at RAM[R13-5]
    ])

    REPOSITION_RETURN_VALUE = '\n'.join([
        POP_STACK_D,
        "@ARG",
        "A=M",
        "M=D",  # return value stored in ARG[0]?
    ])

    RESTORE_CALLER_SP = '\n'.join([
        "@ARG",
        "D=M+1",
        "@SP",
        "M=D",  # SP=ARG+1
    ])

    RESTORE_CALLER_VAR = '\n'.join([
        "@R13",
        "AM=M-1",
        "D=M",
        "@{var}",
        "M=D",  # THAT = *(frame-1)
    ])

    GOTO_RETURN_ADDR = '\n'.join([
        "@R14",
        "A=M",  # RET = *(frame-5)
        "0;JMP"
    ])

    RETURN = '\n'.join([
        SAVE_LOCAL_R13,
        SAVE_RETURN_ADDR_R14,
        REPOSITION_RETURN_VALUE,
        RESTORE_CALLER_SP,
        RESTORE_CALLER_VAR.format(var="THAT"),
        RESTORE_CALLER_VAR.format(var="THIS"),
        RESTORE_CALLER_VAR.format(var="ARG"),
        RESTORE_CALLER_VAR.format(var="LCL"),
        GOTO_RETURN_ADDR,
    ]).split()
