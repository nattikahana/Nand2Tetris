"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Opens the output file and gets ready to write into it

        Args:
            output_stream (typing.TextIO): output stream.
        """
        self.__output_stream = output_stream
        self.__cur_function = None
        self.__file_name = None
        self.__loop_counter = 0
        self.__address_counter = 0

    def set_file_name(self, new_file_name: str) -> None:
        self.__file_name = new_file_name.replace("\\", "/").split("/")[-1]

    def write_arithmetic(self, command: str) -> None:
        """Writes the assembly code that is the translation of the given 
        arithmetic command.

        Args:
            command (str): an arithmetic command.
        """
        self.__output_stream.write("//" + command + "\n")
        if command == "add":
            self.__output_stream.write("@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M+D\n")
        elif command == "sub":
            self.__output_stream.write("@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M-D\n")
        elif command == "neg":
            self.__output_stream.write("@SP\nA=M-1\nM=-M\n")
        elif command == "eq":
            self.__if_eq()
        elif command == "gt":
            self.__if_gt()
        elif command == "lt":
            self.__if_lt()
        elif command == "and":
            self.__output_stream.write("@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D&M\n")
        elif command == "or":
            self.__output_stream.write("@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D|M\n")
        elif command == "not":
            self.__output_stream.write("@SP\nA=M-1\nM=!M\n")

    def __if_lt(self):
        self.__output_stream.write("@SP\nM=M-1\n" +  # sp--
                                   "A=M\nD=M\n" +  # D = y
                                   "@YLT." + self.__file_name + str(
            self.__loop_counter) + "\nD;JLT\n" +  # jump to YLT if y<0
                                   "@SP\nA=M-1\nD=M\n"  # D=x
                                   "@XLTY." + self.__file_name + str(
            self.__loop_counter) + "\nD;JLT\n" +  # jump to XLTY if x<y

                                   "(XMINUSY." + self.__file_name + str(self.__loop_counter) + ")\n" +  # D = x-y
                                   "@SP\nA=M-1\nD=M\nA=A+1\nD=D-M\n" +

                                   "@XLTY." + self.__file_name + str(
            self.__loop_counter) + "\nD;JLT\n" +  # jump to XLTY if x<y

                                   "(XGEY." + self.__file_name +  # x>=y therefore jump to END
                                   str(self.__loop_counter) + ")\n@SP\nA=M-1\nD=M\nM=0\n@END." + self.__file_name +
                                   str(self.__loop_counter) + "\n0;JMP\n" +

                                   "(YLT." + self.__file_name + str(self.__loop_counter) + ")" +  # y<0
                                   "\n@SP\nA=M-1\nD=M\n" +  # D=x

                                   "@XMINUSY." + self.__file_name + str(
            self.__loop_counter) + "\nD;JLT" +  # jump to XMINUSY if x<0

                                   "\n@XGEY." + self.__file_name + str(
            self.__loop_counter) +  # x>=y therefore jump to XGEY (to end)
                                   "\n0;JMP\n" +

                                   "(XLTY." + self.__file_name + str(
            self.__loop_counter) + ")\n@SP\nA=M-1\nM=-1\n" +  # x<y then True
                                   "(END." + self.__file_name + str(self.__loop_counter) + ")\n")  # end
        self.__loop_counter += 1

    def __if_gt(self):
        self.__output_stream.write("@SP\nM=M-1\n" +  # sp--
                                   "A=M\nD=M\n" +  # D = y
                                   "@YGT." + self.__file_name + str(
            self.__loop_counter) + "\nD;JGT\n" +  # jump to YGT if y>0
                                   "@SP\nA=M-1\nD=M\n"  # D=x
                                   "@XGTY." + self.__file_name + str(
            self.__loop_counter) + "\nD;JGT\n" +  # jump to XGTY if x>y

                                   "(XMINUSY." + self.__file_name + str(self.__loop_counter) + ")\n" +  # D = x-y
                                   "@SP\nA=M-1\nD=M\nA=A+1\nD=D-M\n" +

                                   "@XGTY." + self.__file_name + str(
            self.__loop_counter) + "\nD;JGT\n" +  # jump to XGTY if x>y

                                   "(XLEY." + self.__file_name +  # x<=y therefore jump to END
                                   str(self.__loop_counter) +
                                   ")\n@SP\nA=M-1\nD=M\nM=0\n@END." + self.__file_name + str(
            self.__loop_counter) + "\n0;JMP\n" +

                                   "(YGT." + self.__file_name + str(self.__loop_counter) + ")" +  # y>0
                                   "\n@SP\nA=M-1\nD=M\n" +  # D=X

                                   "@XMINUSY." + self.__file_name + str(
            self.__loop_counter) + "\nD;JGT" +  # jump to XMINUSY if x>0

                                   "\n@XLEY." + self.__file_name + str(
            self.__loop_counter) +  # x<=y therefore jump to XLEY (to end)
                                   "\n0;JMP\n" +

                                   "(XGTY." + self.__file_name + str(
            self.__loop_counter) + ")\n@SP\nA=M-1\nM=-1\n" +  # x>y then True
                                   "(END." + self.__file_name + str(self.__loop_counter) + ")\n")  # end
        self.__loop_counter += 1

    def __if_eq(self):
        self.__output_stream.write("@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\nM=0\n" +
                                   "@NEQ." + self.__file_name + str(self.__loop_counter) +
                                   "\nD;JNE\n" + "@SP\nA=M-1\nM=-1\n(NEQ." + self.__file_name +
                                   str(self.__loop_counter) + ")\n")
        self.__loop_counter += 1

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes the assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        command_name = {"C_POP": "pop", "C_PUSH": "push"}
        self.__output_stream.write("//" + command_name[command] + " " + segment + " " +
                                   str(index) + "\n")
        dict_type = {"argument": "ARG", "local": "LCL", "this": "THIS", "that": "THAT"}
        if command == "C_POP":

            if segment in dict_type:
                self.__output_stream.write("@" + dict_type[segment] + "\nD=M\n@" +
                                           str(index) + "\nD=D+A\n@R13\nM=D\n" +
                                           "@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\n" +
                                           "M=D\n")
            if segment == "temp":
                self.__output_stream.write("@R5\nD=A\n@" + str(index) +
                                           "\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\n" +
                                           "A=M\nD=M\n@R13\nA=M\nM=D\n")
            if segment == "static":
                self.__output_stream.write("@SP\nM=M-1\nA=M\nD=M\n@" + self.__file_name +
                                           "." + str(index) + "\nM=D\n")
            if segment == "pointer":
                dict_pointer = {0: "THIS", 1: "THAT"}
                self.__output_stream.write("@SP\nM=M-1\nA=M\nD=M\n@" +
                                           dict_pointer[index] + "\nM=D\n")
        elif command == "C_PUSH":
            if segment in dict_type:
                self.__output_stream.write("@" + dict_type[segment] + "\nD=M\n@" +
                                           str(index) + "\nA=D+A\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n")
            if segment == "temp":
                self.__output_stream.write("@R5\nD=A\n@" + str(index) +
                                           "\nA=D+A\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n")
            if segment == "static":
                self.__output_stream.write("@" + self.__file_name + "." + str(index) +
                                           "\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n")
            if segment == "pointer":
                dict_pointer = {0: "THIS", 1: "THAT"}
                self.__output_stream.write("@" + dict_pointer[index] + "\nD=M\n" +
                                           "@SP\nM=M+1\nA=M-1\nM=D\n")
            if segment == "constant":
                self.__output_stream.write("@" + str(index) +
                                           "\nD=A\n@SP\nM=M+1\nA=M-1\nM=D\n")

    def write_init(self) -> None:
        """Writes the assembly code that effects the VM initialization
        (also called bootstrap code). This code should be placed in the
         ROM beginning in address 0x0000.
         """
        self.__output_stream.write("// initialize the stack pointer to 0x0100\n")
        #  SP=256 // initialize the stack pointer to 0x0100
        self.__output_stream.write("@256\nD=A\n@SP\nM=D\n")
        self.__output_stream.write("// invoke Sys.init\n")
        #  call Sys.init // invoke Sys.init
        self.write_call("Sys.init", 0)

    def write_label(self, label: str) -> None:
        """Writes the assembly code that is the translation of
         the given label command.

        Args:
            label (str): the label to initialize.
        """
        self.__output_stream.write("//label " + label)
        if self.__cur_function:
            self.__output_stream.write("\n(" + self.__cur_function +
                                       "$" + label + ")\n")
        else:
            self.__output_stream.write("\n(" + label + ")\n")

    def write_goto(self, label: str) -> None:
        """Writes the assembly code that is the translation of
         the given goto command.

        Args:
            label (str): the label to goto.
        """
        self.__output_stream.write("//goto " + label)
        if self.__cur_function:
            self.__output_stream.write("\n@" + self.__cur_function +
                                       "$" + label + "\n0;JMP\n")
        else:
            self.__output_stream.write("\n@" + label + "\n0;JMP\n")

        # self.__output_stream.write("\n@" + label + "." + self.__file_name + "\n0;JMP\n")

    def write_if(self, label: str) -> None:
        """Writes the assembly code that is the translation of
         the given if-goto command.

        Args:
            label (str): the label to goto if true.
        """
        self.__output_stream.write("//if-goto " + label)
        self.__output_stream.write("\n@SP\nM=M-1\nA=M\nD=M\n")

        if self.__cur_function:
            self.__output_stream.write("\n@" +
                                       self.__cur_function + "$" + label + "\nD;JNE\n")
        else:
            self.__output_stream.write("\n@" + label + "\nD;JNE\n")

        # self.__output_stream.write("\n@SP\nM=M-1\nA=M\nD=M\n@" +
        #                            label + "." + self.__file_name + "\nD;JNE\n")

    def write_call(self, function_name: str, num_args: int) -> None:
        """Writes the assembly code that is the translation of
         the given call command.

        Args:
            function_name (str): the label to goto if true.
            num_args (int): the number of args the function calls
        """
        self.__output_stream.write("//call  " + function_name + " " + str(num_args))
        #  push return-address (using label below)
        # self.__output_stream.write("\n@RETURN_ADDRESS." + self.__file_name +
        #                            str(self.__address_counter) +
        #                            "\nD=A\n@SP\nM=M+1\nA=M-1\nM=D\n")
        self.__output_stream.write("\n@" + self.__file_name + "." + function_name + "$RET." +
                                   str(self.__address_counter) +
                                   "\nD=A\n@SP\nM=M+1\nA=M-1\nM=D\n")

        #  push LCL  (save LCL of calling function)
        self.__output_stream.write("@LCL\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n")

        #  push ARG (save ARG of calling function)
        self.__output_stream.write("@ARG\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n")

        #  push THIS (save THIS of calling function)
        self.__output_stream.write("@THIS\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n")

        #  push THAT (save THAT of calling function)
        self.__output_stream.write("@THAT\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n")

        #  ARG = SP-n-5 (reposition ARG (n=number of args))
        self.__output_stream.write("@SP\nD=M\n@" + str(num_args) + "\n" +
                                   "D=D-A\n@5\nD=D-A\n@ARG\nM=D\n")

        # LCL = SP (reposition LCL)
        self.__output_stream.write("@SP\nD=M\n@LCL\nM=D\n")

        # goto f (transfer control)
        self.__output_stream.write("@" + function_name + "\n0;JMP\n")

        #  (return-address) label for the return address
        self.__output_stream.write("(" + self.__file_name + "." + function_name + "$RET." +
                                   str(self.__address_counter) + ")\n")
        self.__address_counter += 1

    def write_return(self) -> None:
        """Writes the assembly code that is the translation of
         the given return command.
        """
        self.__output_stream.write("//return\n")

        # FRAME = LCL
        self.__output_stream.write("@LCL\nD=M\n@R15\nM=D\n")
        # RER = *(FRAME - 5)
        self.__output_stream.write("@5\nD=A\n@R15\nD=M-D\nA=D\nD=M\n" +
                                   "@R14\nM=D\n")
        # *ARG = POP()
        self.__output_stream.write("@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\nM=D\n")

        # SP = ARG + 1
        self.__output_stream.write("@ARG\nD=M+1\n@SP\nM=D\n")

        # THAT = *(FRAME -1)
        self.__output_stream.write("@R15\nA=M-1\nD=M\n@THAT\nM=D\n")

        # THIS = *(FRAME -2)
        self.__output_stream.write("@R15\nD=M\n@2\nA=D-A\nD=M\n@THIS\nM=D\n")

        # ARG = *(FRAME -3)
        self.__output_stream.write("@R15\nD=M\n@3\nA=D-A\nD=M\n@ARG\nM=D\n")

        # LCL = *(FRAME -4)
        self.__output_stream.write("@R15\nD=M\n@4\nA=D-A\nD=M\n@LCL\nM=D\n")

        # GO TO RET
        self.__output_stream.write("@R14\nA=M\n0;JMP\n")

    def write_function(self, function_name: str, num_locals: int) -> None:
        """Writes the assembly code that is the translation of
         the given function command.

        Args:=
            function_name (str): the label to goto if true.
            num_locals (int ): the number of locals the function calls
        """
        self.__cur_function = function_name
        self.__output_stream.write("//function " + function_name +
                                   " " + str(num_locals) + "\n")
        self.__output_stream.write("(" + function_name + ")\n")
        for _ in range(num_locals):
            self.write_push_pop("C_PUSH", "constant", 0)
