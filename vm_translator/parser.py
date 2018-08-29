from .utils.cmd_types import CmdTypes


class Parser:
    """Handles the parsing of a single .vmfile.

    Encapsulates access to the input code. It reads VM commands, parses
    them, and provides convenient access to their components. In
    addition, it removes all white space and comments.
    """

    def __init__(self, file):
        """Opens the input stream and gets ready to parse it."""

        self.file = file
        self.cmd = None
        self.eof = False
        self.cmd_type = None
        self.cmd_arg1 = None
        self.cmd_arg2 = None
        self.__enter__()  # might be a bad idea

    def __enter__(self):
        """Allows usage of with Parser(file) as p:

        Enters context.
        """
        self.fd = open(self.file)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Allows usage of with Parser(file) as p:

        Auto-closes file.
        """
        self.fd.close()

    def __iter__(self):
        for line in self.fd:
            self.cmd_type = None  # reset initial values ..
            self.cmd_arg1 = None
            self.cmd_arg2 = None
            self.cmd = line
            self.clean()
            if self.cmd == '':
                continue  # only yield lines with actual code ..
            yield self.cmd
        else:
            self.eof = True
            self.__exit__(None, None, None)  # might be a bad idea

    def clean(self):
        """Remove all whitespace and comments from current line."""

        self.cmd = self.cmd.split("//")[0]
        # self.cmd = ''.join(self.cmd.split())
        self.cmd = self.cmd.strip()  # remove outer whitespace only.

    def has_more_commands(self):
        """Are there more commands in the input?

        :returns: boolean
        """
        return not self.eof

    def advance(self):
        """Reads the next command from the input.

        Makes it the current command. Should be called only if
        'has_more_commands()' is True. Initially there is no current
        command.
        Usage:

        while p.has_more_commands():
            p.advance()
        """

        try:  # kind of hacky ... use for loop instead!
            self.cmd = next(self.__iter__())
        except StopIteration:
            pass

    def command_type(self):
        """Returns the type of the current VM command.

        C_ARITHMETIC is returned for all the arithmetic
        commands.

        :returns: C_ARITHMETIC, C_PUSH, C_POP, C_LABEL, C_GOTO, C_IF, C_FUNCTION, C_RETURN, C_CALL

        Note: sets cmd_type, cmd_arg1, cmd_arg2
        Note: modifies self.cmd
        """
        if self.cmd_type is not None:
            return self.cmd_type  # should be true only after first run ..

        if any([self.cmd == c for c in ("add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not")]):
            self.cmd_type = CmdTypes.C_ARITHMETIC
            self.arg1()  # sets cmd_arg1
            return self.cmd_type
        elif self.cmd[0:4] == "push":
            self.cmd_type = CmdTypes.C_PUSH
            self.arg2()  # sets cmd_arg1, cmd_arg2
            return self.cmd_type
        elif self.cmd[0:3] == "pop":
            self.cmd_type = CmdTypes.C_POP
            self.arg2()  # sets cmd_arg1, cmd_arg2
            return self.cmd_type
        elif self.cmd[0:5] == "label":
            self.cmd_type = CmdTypes.C_LABEL
            self.arg1()
            return self.cmd_type
        elif self.cmd[0:4] == "goto":
            self.cmd_type = CmdTypes.C_GOTO
            self.arg1()
            return self.cmd_type
        elif self.cmd[0:7] == "if-goto":
            self.cmd_type = CmdTypes.C_IF
            self.arg1()
            return self.cmd_type
        elif self.cmd[0:8] == "function":
            self.cmd_type = CmdTypes.C_FUNCTION
            self.arg2()
            return self.cmd_type
        elif self.cmd[0:6] == "return":
            self.cmd_type = CmdTypes.C_RETURN
            return self.cmd_type
        elif self.cmd[0:4] == "call":
            self.cmd_type = CmdTypes.C_CALL
            self.arg2()
            return self.cmd_type
        return None

    def arg1(self):
        """Returns the first arg. of the current command.

        In the case of C_ARITHMETIC, the command itself (add, sub, etc.)
        is returned. Should not be called if the current command is
        C_RETURN.

        :returns: string

        As self.cmd_arg1 is reset each iteration I should be able
        to return it if it exits.
        If there is no self.cmd_type ... I should be able to call it
        and have it only run once.

        Note: sets cmd_type, cmd_arg1, cmd_arg2
        Note: modifies self.cmd
        """

        if self.cmd_arg1 is not None:
            return self.cmd_arg1
        if self.cmd_type is None:
            self.command_type()  # should only run once ...

        if self.cmd_type == CmdTypes.C_ARITHMETIC:
            self.cmd_arg1 = self.cmd
            return self.cmd_arg1
        elif any([self.cmd_type == c for c in (CmdTypes.C_PUSH, CmdTypes.C_POP, CmdTypes.C_FUNCTION, CmdTypes.C_CALL)]):
            self.arg2()  # sets cmd_arg1, cmd_arg2
            return self.cmd_arg1
        elif any([self.cmd_type == c for c in (CmdTypes.C_LABEL, CmdTypes.C_GOTO, CmdTypes.C_IF)]):
            self.cmd, self.cmd_arg1 = self.cmd.split()
            return self.cmd_arg1
        return None

    def arg2(self):
        """Returns the second argument of the current command.

        Should be called only if the current command is C_PUSH, C_POP,
        C_FUNCTION, or C_CALL.

        :returns: int
        Note: sets cmd_type, cmd_arg1, cmd_arg2
        Note: modifies self.cmd
        """

        if self.cmd_arg2 is not None:
            return self.cmd_arg2
        if self.cmd_type is None:
            self.command_type()  # should only run once ...

        if any([self.cmd_type == c for c in (CmdTypes.C_PUSH, CmdTypes.C_POP, CmdTypes.C_FUNCTION, CmdTypes.C_CALL)]):
            self.cmd, self.cmd_arg1, self.cmd_arg2 = self.cmd.split()
            self.cmd_arg2 = int(self.cmd_arg2)
            return self.cmd_arg2
        return None
