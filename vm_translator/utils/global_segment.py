class GlobalSegment:
    @staticmethod
    def pointer_converter(x):
        """Pointer should only refer to RAM[3] or RAM[4], @THIS, @THAT only!"""
        if x in (0, 1):
            return "R{}".format(x+3)
        raise Exception("Pointer must be either 0, or 1, referring to RAM[3], RAM[4].")

    @staticmethod
    def temp_converter(x):
        """Temp is R5-R12."""
        if 0 <= x <= 8:
            return "R{}".format(x+5)
        raise Exception("Temp is:", x, "Temp must be between 0, 8, referring to R5-R12 inclusive.")

    @staticmethod
    def static_converter(x):
        """Each static variable j in file Xxx.vm is translated into the assembly symbol Xxx.j.

        In the subsequent assembly process, these symbolic variables will be
        allocated RAM space by the Hack Assembler.

        {name}.x (or j or i or whatever).
        'name' is filled in by the CodeWriter class.
        """
        return "{name}." + str(x)

    @staticmethod
    def converter(segment, index):
        """Calculate value of segment to use."""
        converter_base = {
            "constant": lambda x: str(x),
            "pointer": GlobalSegment.pointer_converter,
            "temp": GlobalSegment.temp_converter,
            "static": GlobalSegment.static_converter,
        }
        return converter_base[segment](index)
