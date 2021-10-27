"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import os


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Opens the output file and gets ready to write into it

        Args:
            output_stream (typing.TextIO): output stream.
        """
        self.__output_stream = output_stream
        self.command_number = "1"
        self.__input_filename, input_extension = os.path.splitext(os.path.basename(output_stream.name))

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        pass

    def write_arithmetic(self, command: str) -> None:
        """Writes the assembly code that is the translation of the given
        arithmetic command.

        Args:
            command (str): an arithmetic command.
        """
        arithmetic_command_dict = {"add": self.__c_add(command), "sub": self.__c_sub(command),
                                   "neg": self.__c_neg(command), "eq": self.__c_eq(command), "gt": self.__c_gt(command),
                                   "lt": self.__c_lt(command),
                                   "and": self.__c_and(command), "or": self.__c_or(command),
                                   "not": self.__c_not(command)}

        self.__output_stream.write(arithmetic_command_dict[command])
        self.command_number = str(int(self.command_number) + 1)

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes the assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        if command == "C_PUSH":
            self.__output_stream.write(self.__translate_push(segment, index))
        else:
            self.__output_stream.write(self.__translate_pop(segment, index))

    def __translate_push(self, segment, index):
        push_dict = {"local": self.__push_4_seg(index, segment), "argument": self.__push_4_seg(index, segment),
                     "this": self.__push_4_seg(index, segment),
                     "that": self.__push_4_seg(index, segment),
                     "constant": self.__c_push_constant(index), "static": self.__c_push_static(index),
                     "pointer": self.__c_push_pointer(index),
                     "temp": self.__c_push_temp(index)}

        return push_dict[segment]

    def __translate_pop(self, segment, index):

        pop_dict = {"local": self.__pop_4_seg(index, segment), "argument": self.__pop_4_seg(index, segment),
                    "this": self.__pop_4_seg(index, segment),
                    "that": self.__pop_4_seg(index, segment),
                    "static": self.__c_pop_static(index), "pointer": self.__c_pop_pointer(index),
                    "temp": self.__c_pop_temp(index)}

        return pop_dict[segment]

    def close(self) -> None:
        """Closes the output file."""
        # Your code goes here!
        self.__output_stream.close()

    def __c_not(self, command):
        return '//' + command + '\n   @SP\n   A=M-1\n   M=!M\n'

    def __c_or(self, command):
        return '//' + command + '\n   @SP\n   M=M-1\n   A=M-1\n   D=M\n   A=A-1\n   M=D|M\n'

    def __c_and(self, command):
        return '//' + command + '\n   @SP\n   M=M-1\n   A=M-1\n   D=M\n   A=A-1\n   M=D&M\n'

    def __c_lt(self, command):
        return '//' + command + '\n// if (y <= 0):\n   @SP\n   AM=M-1\n   D=M // (D=y)\n   @R13\n   M=D // (M=y)\n' \
                                '   @YPOSITIVE' + self.command_number + '\n   D;JGT\n// if x <= 0:\n   @SP\n   A=M-1\n   D=M // (D=x)\n' \
                                                                        '   @SAMESIGN' + self.command_number + '\n   D;JLE\n   @FALSE' + self.command_number + '\n   0;JMP\n' \
                                                                                                                                                               '(YPOSITIVE' + self.command_number + ')\n   // if x <= 0:\n   @SP\n   A=M-1\n   D=M // (D=x)\n' \
                                                                                                                                                                                                    '   @SAMESIGN' + self.command_number + '\n   D;JGT\n   D=-1\n   @DO' + self.command_number + '\n' \
                                                                                                                                                                                                                                                                                                 '   0;JMP\n(SAMESIGN' + self.command_number + ')\n   @R13\n   D=D-M\n   @FALSE' + self.command_number \
               + '\n   D;JGE\n   D=-1\n   @DO' + self.command_number + '\n   0;JMP\n(FALSE' + self.command_number + \
               ')\n   D=0\n(DO' + self.command_number + ')\n   @SP\n   A=M-1\n   M=D\n'

    def __c_gt(self, command):
        return '//' + command + '\n// if (y <= 0):\n   @SP\n   AM=M-1\n   D=M // (D=y)\n   @R13\n   M=D // (M=y)\n' \
                                '   @YPOSITIVE' + self.command_number + '\n   D;JGT\n// if x <= 0:\n   @SP\n   A=M-1\n' \
                                                                        '   D=M // (D=x)\n   @SAMESIGN' + self.command_number + '\n   D;JLE\n   @TRUE' + self.command_number \
               + '\n   0;JMP\n(YPOSITIVE' + self.command_number + ')\n   // if x <= 0:\n   @SP\n   A=M-1\n' \
                                                                  '   D=M // (D=x)\n   @SAMESIGN' + self.command_number + '\n   D;JGT\n   D=0\n   @DO' + \
               self.command_number + '\n   0;JMP\n(SAMESIGN' + self.command_number + ')\n   @R13\n   D=D-M\n' \
                                                                                     '   @TRUE' + self.command_number + '\n   D;JGT\n   D=0\n   @DO' + self.command_number + '\n   0;JMP\n' \
                                                                                                                                                                             '(TRUE' + self.command_number + ')\n   D=-1\n(DO' + self.command_number + ')\n   @SP\n   A=M-1\n' \
                                                                                                                                                                                                                                                       '   M=D\n'

    def __c_eq(self, command):
        return '//' + command + '\n   @SP\n   AM=M-1\n   A=A-1\n   D=M\n   M=0\n   A=A+1\n   D=M-D\n   @EQ' + self.command_number \
               + '\n   D;JEQ\n   @END' + self.command_number + '\n   0;JMP\n(EQ' + self.command_number + ')\n   @SP\n   A=M-1\n   M=-1\n(END' + self.command_number + ')\n'

    def __c_neg(self, command):
        return '//' + command + '\n   @SP\n   A=M-1\n   M=-M\n'

    def __c_sub(self, command):
        return '//' + command + '\n   @SP\n   M=M-1\n   A=M\n   D=M\n   A=A-1\n   M=M-D\n'

    def __c_add(self, command):
        return '//' + command + '\n   @SP\n   M=M-1\n   A=M\n   D=M\n   A=A-1\n   M=D+M\n'

    def __c_push_static(self, index):
        return '//push static ' + str(
            index) + '\n   @' + self.__input_filename + '.' + str(
            index) + '\n   D=M\n   \n@SP   M=M+1\n   A=M-1\n   M=D\n'

    def __c_push_pointer(self, index):
        return '//push pointer ' + str(index) + '\n   @3\n   D=A\n' \
                                                '   @' + str(
            index) + '\n   A=D+A\n   D=M\n   @SP\n   M=M+1\n   A=M-1\n   M=D\n'

    def __c_push_temp(self, index):
        return '//push temp ' + str(index) + '\n   @5\n   D=A\n' \
                                             '   @' + str(
            index) + '\n   D=D+A\n   @R13\n   M=D\n   A=D\n   D=M\n   @SP\n   M=M+1\n   A=M-1\n   M=D\n'

    def __c_push_constant(self, index):
        return '//push constant ' + str(index) + '\n   @' + str(index) + '\n' \
                                                                         '   D=A\n   @SP\n   M=M+1\n   A=M-1\n   M=D\n'

    def __push_4_seg(self, index, segment):
        seg_dict = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT'}
        return '//push ' + segment + ' ' + str(index) + '\n   @' + seg_dict[segment] + '\n   D=M\n' \
                                                                                       '   @' + str(
            index) + '\n   D=D+A\n   @R13\n   M=D\n   A=D\n   D=M\n   @SP\n   M=M+1\n   A=M-1\n   M=D\n'

    def __c_pop_static(self, index):
        return '//pop static ' + str(
            index) + '\n   @SP\n   AM=M-1\n   D=M\n   @' + self.__input_filename + '.' + str(
            index) + '\n   M=D\n'

    def __c_pop_pointer(self, index):
        return '//pop pointer' + str(index) + '\n   @3\n   D=A\n' \
                                              '   @' + str(
            index) + '\n   D=D+A\n   @R13\n   M=D\n   @SP\n   AM=M-1\n   D=M\n   @R13\n   A=M\n   M=D\n'

    def __c_pop_temp(self, index):
        return '//pop temp' + str(index) + '\n   @5\n   D=A\n' \
                                           '   @' + str(
            index) + '\n   D=D+A\n   @R13\n   M=D\n   @SP\n   AM=M-1\n   D=M\n   @R13\n   A=M\n   M=D\n'

    def __pop_4_seg(self, index, segment):
        seg_dict = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT'}
        return '//pop ' + segment + ' ' + str(index) + '\n   @' + str(index) + '\n   D=M\n' \
                                                                               '   @' + seg_dict[
                   segment] + '\n   D=D+A\n   @R13\n   M=D\n   @SP\n   AM=M-1\n   D=M\n   @R13\n   A=M\n   M=D\n'
