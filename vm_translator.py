import sys
import os

from vm_translator.utils.cmd_types import CmdTypes
from vm_translator.parser import Parser
from vm_translator.code_writer import CodeWriter


class VMTranslator:
    """Translate a directory or file into a single *.asm file.

    VM program may span either a single .vm file or a directory containing one or more .vm files. In the former case, the VM translator is invoked using  VMTranslator fileName.vm. The translator creates an output file named fileName.asm, which is stored in the same directory of the input file. In the latter case, the VM translator is invoked using VMTranslator dirName. The translator creates a single output file named dirName.asm, which is stored in the same directory. This single file contains the assembly code resulting from translating all the .vm files in the input directory. The name of the input file or directory may contain a file path.

    If no path is specified, the VM translator operates on the current directory by default.
    """
    @staticmethod
    def translate(path):
        """Convert a *.vm file (or a folder containing *.vm files) into a single *.asm program.

        Use a single CodeWriter for handling the output.
        Use a separate Parser for handling each input file.
        Converted into one large *.asm file.
        """

        _, name = os.path.split(path)
        out_file = os.path.join(path, name)
        # import pdb;pdb.set_trace()
        with CodeWriter(out_file) as cw:  # write to path/path.asm
            for file, name in VMTranslator.get_files(path):
                with Parser(file) as p:
                    cw.set_file_name(name)
                    for cmd in p:
                        # import pdb;pdb.set_trace()
                        if p.command_type() == CmdTypes.C_ARITHMETIC:
                            cw.write_arithmetic(p.arg1())
                        elif any([p.cmd_type == c for c in (CmdTypes.C_PUSH, CmdTypes.C_POP)]):
                            cw.write_push_pop(p.cmd, p.arg1(), p.arg2())
                        elif p.cmd_type == CmdTypes.C_LABEL:
                            cw.write_label(p.arg1())
                        elif p.cmd_type == CmdTypes.C_IF:
                            cw.write_if(p.arg1())
                        elif p.cmd_type == CmdTypes.C_GOTO:
                            cw.write_goto(p.arg1())
                        elif p.cmd_type == CmdTypes.C_FUNCTION:
                            cw.write_function(p.arg1(), p.arg2())
                        elif p.cmd_type == CmdTypes.C_RETURN:
                            cw.write_return()
                        elif p.cmd_type == CmdTypes.C_CALL:
                            cw.write_call(p.arg1(), p.arg2())
                        else:
                            print("I haven't write code to handle '{}' yet ...".format(cmd))

    @staticmethod
    def get_files(path):
        """Yield path if path is file ending with *.vm

        If path is a file ... must end with .vm
        If file is a directory ... process each *.vm file in directory one by one.

        If file is a directory yield each file in directory ending with
        *.vm.
        """
        if path.endswith('.vm'):
            # second out arg is file name, with file type removed
            yield path, os.path.split(path)[1].rsplit('.')[0]
        else:
            for file in os.listdir(path):
                if file.endswith(".vm"):
                    yield os.path.join(path, file), file.rsplit('.')[0]  # remove file type


if __name__ == "__main__":
    # import pdb;pdb.set_trace()
    if len(sys.argv) == 1:  # Operate on current directory if no path specified.
        VMTranslator.translate(os.path.dirname(__file__))
    elif len(sys.argv) > 1:  # Operate on passed directory or file
        VMTranslator.translate(sys.argv[1])
    else:
        raise Exception("You need to pass in a file name to be translated as the second argument!")
