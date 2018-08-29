from .basic import POP_STACK_D


class LabelIfGoto:
    GOTO = "\n".join([
        "@{symbol}",
        "0;JMP"  # if stack is 1? Maybe pop from stack ...
    ]).split()

    IF_GOTO = "\n".join([
        POP_STACK_D,
        "@{symbol}",
        "D;JNE"  # if stack is 1? Maybe pop from stack ...
    ]).split()

    @staticmethod
    def get_label_symbol(func_name, label):
        return "{}${}".format(func_name or "null", label)
