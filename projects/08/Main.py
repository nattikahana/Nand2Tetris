"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from Parser import Parser
from CodeWriter import CodeWriter


def translate_file(
        input_file: typing.TextIO, output_file: typing.TextIO, file_name: str) -> None:
    """Translates a single file.

    Args:
        input_file (typing.TextIO): the file to translate.
        output_file (typing.TextIO): writes all output to this file.
        input_file (string):
    """
    pars = Parser(input_file)
    c_writer = CodeWriter(output_file)
    c_writer.set_file_name(file_name)
    c_writer.write_init()
    while pars.has_more_commands():
        if pars.command_type() == "C_ARITHMETIC":
            c_writer.write_arithmetic(pars.arg1())
        elif pars.command_type() in ["C_PUSH", "C_POP"]:
            c_writer.write_push_pop(pars.command_type(), pars.arg1(), pars.arg2())
        elif pars.command_type() == "C_LABEL":
            c_writer.write_label(pars.arg1())
        elif pars.command_type() == "C_IF":
            c_writer.write_if(pars.arg1())
        elif pars.command_type() == "C_GOTO":
            c_writer.write_goto(pars.arg1())
        elif pars.command_type() == "C_CALL":
            c_writer.write_call(pars.arg1(), pars.arg2())
        elif pars.command_type() == "C_FUNCTION":
            c_writer.write_function(pars.arg1(), pars.arg2())
        elif pars.command_type() == "C_RETURN":
            c_writer.write_return()
        pars.advance()


if "__main__" == __name__:
    # Parses the input path and calls translate_file on each input file
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: VMtranslator <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_translate = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
        output_path = os.path.join(argument_path, os.path.basename(
            argument_path))
    else:
        files_to_translate = [argument_path]
        output_path, extension = os.path.splitext(argument_path)
    output_path += ".asm"
    with open(output_path, 'w') as output_file:
        for input_path in files_to_translate:
            filename, extension = os.path.splitext(input_path)
            if extension.lower() != ".vm":
                continue
            with open(input_path, 'r') as input_file:
                translate_file(input_file, output_file, filename)
