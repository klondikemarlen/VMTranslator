from .basic import SET_D


class Bootstrap:
    SET_SP = '\n'.join([
        SET_D,
        "@SP",
        "M=D",
    ])

    SET_NEG_VAR = '\n'.join([
        SET_D,
        "@{var}",
        "M=-D",
    ])

    BOOTSTRAP = '\n'.join([
        SET_SP.format(const=256),
        # Setting the LCL, ARG, THIS and THAT point­ers to known illegal
        # values helps identify when a pointer is used before it is initialized.
        SET_NEG_VAR.format(var='LCL', const=1),
        SET_NEG_VAR.format(var='ARG', const=2),
        SET_NEG_VAR.format(var='THIS', const=3),
        SET_NEG_VAR.format(var='THAT', const=4),
    ]).split()
