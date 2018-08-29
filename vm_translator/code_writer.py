import os

from .utils.arithmetic import ArithmeticCode
from .utils.push_pop import PushPopCodes
from .utils.global_segment import GlobalSegment
from .utils.label_if_goto import LabelIfGoto
from .utils.function_return import FunctionReturn
from .utils.call import Call
from .utils.bootstrap import Bootstrap


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, file):
        """Opens the output file/stream and gets ready to write into it."""
        self.file = file  # maybe should be a folder?
        self.file = self.file.rsplit('.')[0] + ".asm"
        self.name = None
        self.func_name = None
        self.if_count = 0
        self.call_count = 0

    def __enter__(self):
        self.fd = open(self.file, 'w')
        # self.write_bootstrap()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fd.close()

    def close(self):
        """Closes the output file."""
        self.__exit__(None, None, None)

    def set_file_name(self, name):
        """Informs the code writer that the translation of a new VM file
        is started.

        I think maybe functions are stored in special files?
        Ah! This is so that I can convert all files in a directory ...
        """

        self.name = name
        self.func_name = None  # reset self.func_name?

    def write_line(self, line):
        """Conveniently append appropriate linesep to line.

        Indent all non-label lines.
        The data should be very pure at this point so complex
        checking is not required.
        """

        if line[0] != "(":  # indent all non-label lines.
            line = " " * 4 + line
        self.fd.write(line)
        self.fd.write(os.linesep)

    def write_bootstrap(self):
        """Writes assembly code that effects the VM initialization.

        Also called 'bootstrap code'. This code must be placed at the beginning
        of the output file.

        SP = 256   // initialize the stack pointer to 0x0100
        call Sys.init   // call the function that calls Main.main

        I'm not really sure if current state of program needs to be saved
        or if SP=261 and nothing else?
        Or even that all LCL, ARG, THIS, THAT should be set to 0?
        """

        for line in Bootstrap.BOOTSTRAP:
            self.write_line(line)

        self.write_call("Sys.init", 0)

    def write_arithmetic(self, command):
        """Writes the assembly code that is the translation of the given
        arithmetic command."""

        # translate step ... dictionary?
        asm_code = ArithmeticCode.CONVERSION[command]
        # import pdb;pdb.set_trace()
        for line in asm_code:
            if "{}" in line:
                line = line.format(self.if_count)
            self.write_line(line)
        self.if_count += 1

    def write_push_pop(self, command, segment, index):
        """Writes the assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP.
        """

        seg_code, asm_code = PushPopCodes.CONVERSION[command][segment]  # [compute_index]
        if any([segment == global_ for global_ in ('static', 'constant', 'temp', 'pointer')]):
            seg_code = GlobalSegment.converter(segment, index)
            seg_code = seg_code.format(name=self.name)
        # import pdb;pdb.set_trace()
        for line in asm_code:
            line = line.format(const=index, seg=seg_code)  # But only if {const} or {seg} exists!
            self.write_line(line)

    def write_label(self, label):
        """Writes the assembly code that effects the 'label' command.

        Format: functionName$label
        Each label 'b' command in a VM function 'f' should generate a globally
        unique symbol 'f$b' where 'f' is the function name and 'b' is the
        label symbol within the VM function's code. When translating 'goto b'
        and 'if-goto b' VM commands into the target language, the full label
        specification 'f$b' must be used instead of 'b'.
        """

        symbol = LabelIfGoto.get_label_symbol(self.func_name, label)
        asm_code = "({})".format(symbol)
        self.write_line(asm_code)

    def write_goto(self, label):
        """Write assembly code that effect the 'goto' command.

        NOTE: my use of "\n".join([]).split() ... allows me to
        chain custom command patterns together. For examples see the
        utils module.
        """

        symbol = LabelIfGoto.get_label_symbol(self.func_name, label)
        for line in LabelIfGoto.GOTO:
            line = line.format(symbol=symbol)
            self.write_line(line)

    def write_if(self, label):
        """Write assembly code that effects the 'if-goto' command."""

        symbol = LabelIfGoto.get_label_symbol(self.func_name, label)
        for line in LabelIfGoto.IF_GOTO:
            line = line.format(symbol=symbol)
            self.write_line(line)

    def write_call(self, function_name, num_args):
        """Write assembly code that is the translation of the 'call' command.

        Format: 'return-address'
        Each VM function call should generate and insert into the
        translated code a unique symbol that serves as a return address,
        namely the memory location (in the target platform's memory) of
        the command following the function call.

        In the course of implementing the code of 'f' (the caller), we
        arrive at the command 'call g nArgs'.
        We assume that nArgs arguments have been pushed onto the stack.
        What do we do next? We generate a symbol, let’s call it
        'returnAddress';
        Next, we effect the following logic:
            push returnAddress // saves the return address
            push LCL           // saves the LCL of f
            push ARG           // saves the ARG of f
            push THIS          // saves the THIS of f
            push THAT          // saves the THAT of f
            ARG = SP-nArgs-5   // repositions SP for g
            LCL = SP           // repositions LCL for g
            goto g             // transfers control to g
            returnAddress:     // the generated symbol
        """
        asm_code = Call.CALL
        # import pdb;pdb.set_trace()
        for line in asm_code:
            line = line.format(call_count=self.call_count, const=num_args, func=function_name)
            self.write_line(line)
        self.call_count += 1

    def write_return(self):
        """Write assembly code that is the translation of the 'return' command.

        In the course of implementing the code of 'g', we arrive to the
        command 'return'. We assume that a return value has been pushed
        onto the stack.
        We effect the following logic:
        frame = LCL          // frame is a temp. variable
        retAddr = *(frame-5) // retAddr is a temp. variable
        *ARG = pop           // repositions the return value
                             // for the caller
        SP=ARG+1             // restores the caller’s SP
        THAT = *(frame-1)    // restores the caller’s THAT
        THIS = *(frame-2)    // restores the caller’s THIS
        ARG = *(frame-3)     // restores the caller’s ARG
        LCL = *(frame-4)     // restores the caller’s LCL
        goto retAddr         // goto returnAddress
        """
        asm_code = FunctionReturn.RETURN
        for line in asm_code:
            self.write_line(line)
        # self.func_name = None  # reset self.func_name

    def write_function(self, function_name, num_locals):
        """Write assembly code that is the trans. of the given 'function' command.

        Format: (functionName)
        Each VM function 'f' should generate a symbol 'f' that refers to
        its entry point in the instruction memory register.

        To implement the command 'function f k'
        we effect the following logic:
        (f)
            repeat k times:
            PUSH 0

        Consider using proper indentation?
        """
        self.func_name = function_name  # activate function name
        asm_code = ["({})".format(self.func_name or "null")]
        asm_code += FunctionReturn.setup_n_local(num_locals)
        for line in asm_code:
            self.write_line(line)


