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
        self.__file_name = output_stream.name.replace("\\", "/").split("/")[-1][:-4]
        self.__loop_counter = 0

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
            self.__output_stream.write("@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\nM=0\n" +
                                       "@NEQ" + str(self.__loop_counter) +
                                       "\nD;JNE\n" + "@SP\nA=M-1\nM=-1\n(NEQ" +
                                       str(self.__loop_counter) + ")\n")
            self.__loop_counter += 1
        elif command == "gt":
            self.__output_stream.write("@SP\nM=M-1\n" +  # sp--
                                       "A=M\nD=M\n" +  # D = y
                                       "@YGT" + str(self.__loop_counter) + "\nD;JGT\n" +  # jump to YGT if y>0
                                       "@SP\nA=M-1\nD=M\n"  # D=x
                                       "@XGTY" + str(self.__loop_counter) + "\nD;JGT\n" +  # jump to XGTY if x>y

                                       "(XMINUSY" + str(self.__loop_counter) + ")\n" +  # D = x-y
                                       "@SP\nA=M-1\nD=M\nA=A+1\nD=D-M\n" +

                                       "@XGTY" + str(self.__loop_counter) + "\nD;JGT\n" +  # jump to XGTY if x>y

                                       "(XLEY" +  # x<=y therefore jump to END
                                       str(self.__loop_counter) +
                                       ")\n@SP\nA=M-1\nD=M\nM=0\n@END" + str(self.__loop_counter) + "\n0;JMP\n" +

                                       "(YGT" + str(self.__loop_counter) + ")" +  # y>0
                                       "\n@SP\nA=M-1\nD=M\n" +  # D=X

                                       "@XMINUSY" + str(self.__loop_counter) + "\nD;JGT" +  # jump to XMINUSY if x>0

                                       "\n@XLEY" + str(self.__loop_counter) +  # x<=y therefore jump to XLEY (to end)
                                       "\n0;JMP\n" +

                                       "(XGTY" + str(self.__loop_counter) + ")\n@SP\nA=M-1\nM=-1\n" +  # x>y then True
                                       "(END" + str(self.__loop_counter) + ")\n")  # end
            self.__loop_counter += 1
        elif command == "lt":
            self.__output_stream.write("@SP\nM=M-1\n" +  # sp--
                                       "A=M\nD=M\n" +  # D = y
                                       "@YLT" + str(self.__loop_counter) + "\nD;JLT\n" +  # jump to YLT if y<0
                                       "@SP\nA=M-1\nD=M\n"  # D=x
                                       "@XLTY" + str(self.__loop_counter) + "\nD;JLT\n" +  # jump to XLTY if x<y

                                       "(XMINUSY" + str(self.__loop_counter) + ")\n" +  # D = x-y
                                       "@SP\nA=M-1\nD=M\nA=A+1\nD=D-M\n" +

                                       "@XLTY" + str(self.__loop_counter) + "\nD;JLT\n" +  # jump to XLTY if x<y

                                       "(XGEY" +   # x>=y therefore jump to END
                                       str(self.__loop_counter) + ")\n@SP\nA=M-1\nD=M\nM=0\n@END" +
                                       str(self.__loop_counter) + "\n0;JMP\n" +

                                       "(YLT" + str(self.__loop_counter) + ")" +  # y<0
                                       "\n@SP\nA=M-1\nD=M\n" +  # D=x

                                       "@XMINUSY" + str(self.__loop_counter) + "\nD;JLT" +  # jump to XMINUSY if x<0

                                       "\n@XGEY" + str(self.__loop_counter) +  # x>=y therefore jump to XGEY (to end)
                                       "\n0;JMP\n" +

                                       "(XLTY" + str(self.__loop_counter) + ")\n@SP\nA=M-1\nM=-1\n" +  # x<y then True
                                       "(END" + str(self.__loop_counter) + ")\n")  # end
            self.__loop_counter += 1
        elif command == "and":
            self.__output_stream.write("@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D&M\n")
        elif command == "or":
            self.__output_stream.write("@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D|M\n")
        elif command == "not":
            self.__output_stream.write("@SP\nA=M-1\nM=!M\n")

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
