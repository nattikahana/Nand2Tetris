"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import JackTokenizer
from VMWriter import VMWriter
from SymbolTable import SymbolTable


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """
    KIND_DICT = {"STATIC": "STATIC", "FIELD": "THIS", "ARG": "ARG", "VAR": "LOCAL"}

    def __init__(self, input_stream: typing.TextIO,
                 output_stream: typing.TextIO) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        self.__cur_args = 0
        self.__if_index = 0
        self.__while_index = 0
        self.__vm_writer = VMWriter(output_stream)
        self.__token = JackTokenizer(input_stream)
        self.__symbol_table = SymbolTable()
        self.__class_name = None
        self.__indentation = ""

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.__token.advance()
        self.__token.advance()
        self.__class_name = self.__token.identifier()
        self.__token.advance()
        self.__token.advance()
        while self.__token.token_type() == "KEYWORD" and self.__token.keyword() in ["STATIC", "FIELD"]:
            self.compile_class_var_dec()
        while self.__token.token_type() == "KEYWORD" and \
                self.__token.keyword() in ["METHOD", "FUNCTION", "CONSTRUCTOR"]:
            self.compile_subroutine()

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        kind = self.__token.keyword().lower()
        self.__token.advance()

        if self.__token.token_type() == "KEYWORD":
            type_ = self.__token.keyword().lower()
        else:
            type_ = self.__token.identifier()
        self.__token.advance()
        self.__symbol_table.define(self.__token.identifier(), type_, kind.upper())
        self.__token.advance()
        while self.__token.symbol() == ",":
            self.__token.advance()
            self.__symbol_table.define(self.__token.identifier(), type_, kind.upper())
            self.__token.advance()
        self.__token.advance()

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function, or constructor."""
        self.__symbol_table.start_subroutine()
        key = self.__token.keyword()
        if key == "METHOD":
            self.__symbol_table.define("this", self.__class_name, "ARG")
        self.__token.advance()
        self.__token.advance()
        identifier = self.__token.identifier()
        self.__token.advance()
        self.__token.advance()
        self.compile_parameter_list()
        self.__token.advance()
        self.__token.advance()
        while self.__token.keyword() == "VAR":
            self.compile_var_dec()
        func_name = self.__class_name + "." + identifier
        self.__vm_writer.write_function(func_name, self.__symbol_table.var_count("VAR"))
        if key == "METHOD":
            # self.__symbol_table.define("this", self.__class_name, "ARG")
            self.__vm_writer.write_push("ARG", 0)
            self.__vm_writer.write_pop("POINTER", 0)
        elif key == "CONSTRUCTOR":
            self.__vm_writer.write_push("CONST", self.__symbol_table.var_count("FIELD"))
            self.__vm_writer.write_call("Memory.alloc", 1)
            self.__vm_writer.write_pop("POINTER", 0)
        # self.compile_parameter_list()
        self.compile_statements()
        self.__token.advance()

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the
        enclosing "()".
        """
        while not (self.__token.token_type() == "SYMBOL" and self.__token.symbol() == ")"):
            type_ = ""
            if self.__token.token_type() == "SYMBOL" and self.__token.symbol() == ",":
                self.__token.advance()
            if self.__token.token_type() == "KEYWORD":
                type_ = self.__token.keyword().lower()
            elif self.__token.token_type() == "IDENTIFIER":
                a = self.__symbol_table.type_of(self.__token.identifier())
                b = self.__token.identifier()
                type_ = self.__token.identifier()

            self.__token.advance()
            name = self.__token.identifier()
            # if type_:
            self.__symbol_table.define(name, type_, "ARG")
            self.__token.advance()

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.__token.advance()
        if self.__token.token_type() == "KEYWORD":
            type_ = self.__token.keyword().lower()
        else:
            type_ = self.__token.identifier()
        self.__token.advance()
        self.__symbol_table.define(self.__token.identifier(), type_, "VAR")
        self.__token.advance()
        while self.__token.symbol() == ",":
            self.__token.advance()
            self.__symbol_table.define(self.__token.identifier(), type_, "VAR")
            self.__token.advance()
        self.__token.advance()

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing
        "{}".
        """
        while not (self.__token.token_type() == "SYMBOL" and self.__token.symbol() == "}"):
            if self.__token.keyword() == "LET":
                self.compile_let()
            elif self.__token.keyword() == "DO":
                self.compile_do()
            elif self.__token.keyword() == "RETURN":
                self.compile_return()
            elif self.__token.keyword() == "IF":
                self.compile_if()
            elif self.__token.keyword() == "WHILE":
                self.compile_while()

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.__token.advance()
        ident = self.__token.identifier()
        self.__token.advance()
        func_name = self.__class_name + "." + ident
        flag = True
        if self.__token.token_type() == "SYMBOL" and self.__token.symbol() == ".":
            self.__token.advance()  # .
            if self.__symbol_table.kind_of(ident) is None:
                func_name = ident + "." + self.__token.identifier()
                flag = False
            else:
                type_ = self.__symbol_table.type_of(ident)
                kind = self.__symbol_table.kind_of(ident)
                index = self.__symbol_table.index_of(ident)

                # self.__symbol_table.define("this", type_, "ARG")
                func_name = type_ + "." + self.__token.identifier()
                self.__vm_writer.write_push(kind, index)
            self.__token.advance()
            self.__token.advance()
            self.compile_expression_list()
        else:
            # self.__symbol_table.define("this", self.__class_name, "ARG")
            self.__token.advance()
            self.__vm_writer.write_push("POINTER", 0)
            self.compile_expression_list()
        self.__token.advance()
        self.__token.advance()
        if flag:
            self.__cur_args += 1
        self.__vm_writer.write_call(func_name, self.__cur_args)
        self.__vm_writer.write_pop("TEMP", 0)

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.__token.advance()
        ident = self.__token.identifier()
        self.__token.advance()
        kind = self.__symbol_table.kind_of(ident)
        index = self.__symbol_table.index_of(ident)
        if self.__token.token_type() == "SYMBOL" and self.__token.symbol() == "[":
            self.__vm_writer.write_push(self.KIND_DICT[kind], index)
            self.__token.advance()
            self.compile_expression()
            self.__vm_writer.write_arithmetic("ADD")
            self.__token.advance()  # ]
            self.__token.advance()  # =
            self.compile_expression()
            self.__vm_writer.write_pop("TEMP", 0)
            self.__vm_writer.write_pop("POINTER", 1)
            self.__vm_writer.write_push("TEMP", 0)
            self.__vm_writer.write_pop("THAT", 0)
            self.__token.advance()
        else:
            self.__token.advance()  # =
            self.compile_expression()
            self.__vm_writer.write_pop(self.KIND_DICT[kind], index)
            self.__token.advance()

    def compile_while(self) -> None:
        """Compiles a while statement."""
        index = str(self.__while_index)
        self.__while_index += 1
        self.__token.advance()
        self.__vm_writer.write_label("WHILE_TRUE" + index)
        self.__token.advance()
        self.compile_expression()
        self.__vm_writer.write_arithmetic("NOT")
        self.__token.advance()
        self.__vm_writer.write_if("WHILE_FALSE" + index)
        self.__token.advance()
        self.compile_statements()
        self.__vm_writer.write_goto("WHILE_TRUE" + index)
        self.__token.advance()
        self.__vm_writer.write_label("WHILE_FALSE" + index)

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.__token.advance()
        if not (self.__token.token_type() == "SYMBOL" and self.__token.symbol() == ";"):
            self.compile_expression()
        else:
            self.__vm_writer.write_push("CONST", 0)
        self.__vm_writer.write_return()
        self.__token.advance()

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        index = str(self.__if_index)
        self.__if_index += 1
        self.__token.advance()
        self.__token.advance()
        self.compile_expression()
        self.__vm_writer.write_arithmetic("NOT")
        self.__vm_writer.write_if("IF_FALSE" + index)
        self.__token.advance()
        self.__token.advance()
        self.compile_statements()
        self.__token.advance()
        self.__vm_writer.write_goto("IF_TRUE" + index)
        self.__vm_writer.write_label("IF_FALSE" + index)

        if self.__token.token_type() == "KEYWORD" and self.__token.keyword() == "ELSE":
            self.__token.advance()
            self.__token.advance()
            self.compile_statements()
            self.__token.advance()

        self.__vm_writer.write_label("IF_TRUE" + index)

    def compile_expression(self) -> None:
        """Compiles an expression."""
        self.compile_term()
        arithmetics = {"&lt;": "LT", "&gt;": "GT", "&amp;": "AND", "+": "ADD",
                       "-": "SUB", "|": "OR", "=": "EQ", "*": "call", "/": "call"}

        while self.__token.token_type() == "SYMBOL" and self.__token.symbol() in arithmetics:
            symbol = self.__token.symbol()
            self.__token.advance()
            self.compile_term()
            if arithmetics[symbol] == "call":
                if symbol == "*":
                    self.__vm_writer.write_call("Math.multiply", 2)
                elif symbol == "/":
                    self.__vm_writer.write_call("Math.divide", 2)
            else:
                self.__vm_writer.write_arithmetic(arithmetics[symbol])

    def compile_term(self) -> None:
        """Compiles a term.
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        if self.__token.token_type() == "STRING_CONST":
            self.__vm_writer.write_push("CONST", len(self.__token.string_val()[1:-1]))
            self.__vm_writer.write_call("String.new", 1)
            for char in self.__token.string_val()[1:-1]:
                self.__vm_writer.write_push("CONST", ord(char))
                self.__vm_writer.write_call("String.appendChar", 2)
            self.__token.advance()
        elif self.__token.token_type() == "INT_CONST":
            self.__vm_writer.write_push("CONST", self.__token.int_val())
            self.__token.advance()
        elif self.__token.token_type() == "KEYWORD":
            if self.__token.keyword() in ["FALSE", "NULL"]:
                self.__vm_writer.write_push("CONST", 0)
            elif self.__token.keyword() == "TRUE":
                self.__vm_writer.write_push("CONST", 0)
                self.__vm_writer.write_arithmetic("NOT")
            elif self.__token.keyword() == "THIS":
                self.__vm_writer.write_push("POINTER", 0)
            self.__token.advance()
        elif self.__token.token_type() == "IDENTIFIER":
            ident = self.__token.identifier()
            self.__token.advance()
            is_method = True
            if self.__token.token_type() == "SYMBOL" and self.__token.symbol() == ".":
                self.__token.advance()
                a = self.__token.symbol()
                if self.__symbol_table.kind_of(ident) is None:
                    name = ident + "." + self.__token.identifier()
                    is_method = False
                else:
                    kind = self.__symbol_table.kind_of(ident)
                    index = self.__symbol_table.index_of(ident)
                    type_ = self.__symbol_table.type_of(ident)
                    # self.__symbol_table.define("this", type_, "ARG")
                    self.__vm_writer.write_push(kind, index)
                    name = type_ + "." + self.__token.identifier()
                self.__token.advance()
                self.__token.advance()
                self.compile_expression_list()
                self.__token.advance()
                if is_method:
                    self.__cur_args += 1
                args = self.__cur_args
                self.__vm_writer.write_call(name, args)
            elif self.__token.token_type() == "SYMBOL" and self.__token.symbol() == "[":
                segment = self.__symbol_table.kind_of(ident)
                index = self.__symbol_table.index_of(ident)
                self.__vm_writer.write_push(segment, index)
                self.__token.advance()
                self.compile_expression()
                self.__vm_writer.write_arithmetic("ADD")
                self.__vm_writer.write_pop("POINTER", 1)
                self.__token.advance()
                self.__vm_writer.write_push("THAT", 0)
            elif self.__token.token_type() == "SYMBOL" and self.__token.symbol() == "(":
                # self.__symbol_table.define("this", self.__class_name, "ARG")
                self.__vm_writer.write_push("POINTER", 0)
                self.__token.advance()
                self.compile_expression_list()
                self.__token.advance()
                func_name = self.__class_name + "." + ident
                self.__vm_writer.write_call(func_name, self.__cur_args + 1)
            else:
                kind = self.__symbol_table.kind_of(ident)
                index = self.__symbol_table.index_of(ident)
                self.__vm_writer.write_push(kind, index)
        elif self.__token.token_type() == "SYMBOL" and self.__token.symbol() == "(":
            self.__token.advance()
            self.compile_expression_list()
            self.__token.advance()
        elif self.__token.token_type() == "SYMBOL" and self.__token.symbol() in "~-":
            symbol = self.__token.symbol()
            self.__token.advance()
            self.compile_term()
            if symbol == "-":
                self.__vm_writer.write_arithmetic("NEG")
            if symbol == "~":
                self.__vm_writer.write_arithmetic("NOT")

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        cur_args = 0
        if not (self.__token.token_type() == "SYMBOL" and self.__token.symbol() == ")"):
            cur_args += 1
            self.compile_expression()
        while not (self.__token.token_type() == "SYMBOL" and self.__token.symbol() == ")"):
            cur_args += 1
            self.__token.advance()
            a = self.__token.symbol()
            self.compile_expression()
        self.__cur_args = cur_args
