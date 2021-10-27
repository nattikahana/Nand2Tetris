"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

ARITHMETICS = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
COMMANDS_DICT = {"push": "C_PUSH", "pop": "C_POP", "label": "C_LABEL",
                 "goto": "C_GOTO", "if": "C_IF", "function": "C_FUNCTION",
                 "return": "C_RETURN", "call": "C_CALL"}
COMMENT = "//"


class Parser:
    """
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        lines = input_file.read().splitlines()
        new_lines = [line if line.find(COMMENT) == -1 else line[:line.find(COMMENT)] for line in lines]
        self.__input_lines = [' '.join(line.split()) for line in new_lines if ''.join(line.split()) != '']
        self.__command_counter = 0

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self.__command_counter < len(self.__input_lines)

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current 
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        self.__command_counter += 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        command = self.__input_lines[self.__command_counter]
        if command in ARITHMETICS:
            return "C_ARITHMETIC"
        return COMMANDS_DICT[command.split()[0]]

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        command = self.__input_lines[self.__command_counter]
        if self.command_type() == "C_ARITHMETIC":
            return command
        else:
            return command.split()[0] + " " + command.split()[1]

    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        command = self.__input_lines[self.__command_counter]
        return int(command.split()[2])
