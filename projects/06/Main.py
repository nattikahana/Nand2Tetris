"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def pass1(s_table, pars):
    """Go through the assembly program, and build the symbol table without generating any code.

    Args:
        s_table: holds a table with symbols and their numeric addresses.
        pars: holds all commands
    """
    commands_counter = 0
    for i in range(16):
        s_table.add_entry("R" + str(i), i)
    s_table.add_entry("SP", 0)
    s_table.add_entry("LCL", 1)
    s_table.add_entry("ARG", 2)
    s_table.add_entry("THIS", 3)
    s_table.add_entry("THAT", 4)
    s_table.add_entry("SCREEN", 16384)
    s_table.add_entry("KBD", 24576)
    while pars.has_more_commands():
        if pars.command_type() == "L_COMMAND":
            if not s_table.contains(pars.symbol()):
                s_table.add_entry(pars.symbol(), commands_counter)
        else:
            commands_counter += 1
        pars.advance()


def pass2(s_table, pars, output_file):
    """Go again through the program, and parse each line.

    Args:
        s_table: holds a table with symbols and their numeric addresses.
        pars: holds all commands
        output_file: writes all output to this file.
    """
    table_counter = 16
    while pars.has_more_commands():
        if pars.command_type() == "A_COMMAND":
            if pars.symbol().isnumeric():
                output_file.write("{0:016b}".format(int(pars.symbol())) + "\n")
            elif s_table.contains(pars.symbol()):
                output_file.write("{0:016b}".format(s_table.get_address(pars.symbol())) + "\n")
            else:
                s_table.add_entry(pars.symbol(), table_counter)
                output_file.write("{0:016b}".format(table_counter) + "\n")
                table_counter += 1
        elif pars.command_type() == "C_COMMAND":
            output_file.write("111" + Code.comp(pars.comp()) +
                              Code.dest(pars.dest()) + Code.jump(pars.jump()) + "\n")
        pars.advance()


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    s_table = SymbolTable()
    pars = Parser(input_file)
    pass1(s_table, pars)
    pars.start_over()
    pass2(s_table, pars, output_file)


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
