"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

BEFORE_JMP = ";"

C_COMMAND = "C_COMMAND"
L_COMMAND = "L_COMMAND"
A_COMMAND = "A_COMMAND"
P_COMMAND = "("
SYMBOL = "@"
AFTER_DEST = "="
COMMENT = "//"


class Parser:
    """Encapsulates access to the input code. Reads and assembly language 
    command, parses it, and provides convenient access to the commands 
    components (fields and symbols). In addition, removes all white space and 
    comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        lines = input_file.read().splitlines()
        new_lines = [line if line.find(COMMENT) == -1 else line[:line.find(COMMENT)] for line in lines]
        self.__input_lines = [''.join(line.split()) for line in new_lines if ''.join(line.split())]
        self.__command_counter = 0

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self.__command_counter < len(self.__input_lines)

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        self.__command_counter += 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        if self.__input_lines[self.__command_counter].startswith(SYMBOL):
            return A_COMMAND
        elif self.__input_lines[self.__command_counter].startswith(P_COMMAND):
            return L_COMMAND
        else:
            return C_COMMAND

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        command = self.__input_lines[self.__command_counter]
        if self.command_type() == L_COMMAND:
            command = command[:-1]
        return command[1:]

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        command = self.__input_lines[self.__command_counter]
        if command.find(AFTER_DEST) == -1:
            return ""
        return command[:command.find(AFTER_DEST)]

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        command = self.__input_lines[self.__command_counter]
        first = 0
        last = len(command)
        if command.find(AFTER_DEST) != -1:
            first = command.find(AFTER_DEST) + 1
        if command.find(BEFORE_JMP) != -1:
            last = command.find(BEFORE_JMP)
        return command[first:last]

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        command = self.__input_lines[self.__command_counter]
        if command.find(BEFORE_JMP) != -1:
            return command[command.find(BEFORE_JMP) + 1:]
        return ""

    def start_over(self):
        """
        Start over the commands from the input and makes the first command the current command.
        """
        self.__command_counter = 0
