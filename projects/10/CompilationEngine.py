"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import JackTokenizer


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: typing.TextIO,
                 output_stream: typing.TextIO) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        self.__output_lines = output_stream
        self.__token = JackTokenizer(input_stream)
        self.__indentation = ""

    def __add_sub_indentation(self, to_add):
        if to_add:
            self.__indentation += "  "
        else:
            self.__indentation = self.__indentation[:-2]

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.__token.advance()
        # self.__token.advance()
        self.__output_lines.write("<class>\n  <keyword> class </keyword>\n")
        self.__add_sub_indentation(True)
        self.__token.advance()
        self.__output_lines.write("  <identifier> " + self.__token.identifier() + " </identifier>\n")
        self.__token.advance()
        self.__output_lines.write("  <symbol> { </symbol>\n")
        self.__token.advance()
        while self.__token.token_type() == "KEYWORD" and self.__token.keyword() in ["STATIC", "FIELD"]:
            self.compile_class_var_dec()
        while self.__token.token_type() == "KEYWORD" and \
                self.__token.keyword() in ["METHOD", "FUNCTION", "CONSTRUCTOR"]:
            self.compile_subroutine()
        self.__output_lines.write("  <symbol> } </symbol>\n")
        self.__output_lines.write("</class>\n")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""

        self.__output_lines.write(self.__indentation + "<classVarDec>\n")
        self.__add_sub_indentation(True)
        self.__output_lines.write(self.__indentation + "<keyword> " +
                                  self.__token.keyword().lower() + " </keyword>\n")
        self.__token.advance()

        if self.__token.token_type() == "KEYWORD":
            self.__output_lines.write(self.__indentation + "<keyword> " +
                                      self.__token.keyword().lower() + " </keyword>\n")
        else:
            self.__output_lines.write(self.__indentation + "<identifier> " +
                                      self.__token.identifier() + " </identifier>\n")
        self.__token.advance()
        self.__output_lines.write(self.__indentation + "<identifier> " +
                                  self.__token.identifier() + " </identifier>\n")
        self.__token.advance()
        while self.__token.symbol() == ",":
            self.__output_lines.write(self.__indentation + "<symbol> , </symbol>\n")
            self.__token.advance()
            self.__output_lines.write(self.__indentation + "<identifier> " +
                                      self.__token.identifier() + " </identifier>\n")
            self.__token.advance()
        self.__output_lines.write(self.__indentation + "<symbol> ; </symbol>\n")
        self.__token.advance()
        self.__add_sub_indentation(False)
        self.__output_lines.write(self.__indentation + "</classVarDec>\n")

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function, or constructor."""
        self.__output_lines.write(self.__indentation + "<subroutineDec>\n")
        self.__add_sub_indentation(True)
        self.__output_lines.write(self.__indentation + "<keyword> " +
                                  self.__token.keyword().lower() + " </keyword>\n")
        self.__token.advance()
        if self.__token.token_type() == "KEYWORD":
            self.__output_lines.write(self.__indentation + "<keyword> " +
                                      self.__token.keyword().lower() + " </keyword>\n")
        else:
            self.__output_lines.write(self.__indentation + "<identifier> " +
                                      self.__token.identifier() + " </identifier>\n")
        self.__token.advance()
        self.__output_lines.write(self.__indentation + "<identifier> " +
                                  self.__token.identifier() + " </identifier>\n")
        self.__token.advance()
        self.__output_lines.write(self.__indentation + "<symbol> ( </symbol>\n")
        self.__token.advance()
        self.compile_parameter_list()
        self.__output_lines.write(self.__indentation + "<symbol> ) </symbol>\n")
        self.__token.advance()
        self.__output_lines.write(self.__indentation + "<subroutineBody>\n")
        self.__add_sub_indentation(True)
        self.__output_lines.write(self.__indentation + "<symbol> { </symbol>\n")
        self.__token.advance()
        while self.__token.keyword() == "VAR":
            self.compile_var_dec()
        self.compile_statements()
        self.__output_lines.write(self.__indentation + "<symbol> } </symbol>\n")
        self.__token.advance()
        self.__add_sub_indentation(False)
        self.__output_lines.write(self.__indentation + "</subroutineBody>\n")
        self.__add_sub_indentation(False)
        self.__output_lines.write(self.__indentation + "</subroutineDec>\n")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the
        enclosing "()".
        """
        self.__output_lines.write(self.__indentation + "<parameterList>\n")
        self.__add_sub_indentation(True)
        while not (self.__token.token_type() == "SYMBOL" and self.__token.symbol() == ")"):
            if self.__token.token_type() == "KEYWORD":
                self.__output_lines.write(self.__indentation + "<keyword> " +
                                          self.__token.keyword().lower() + " </keyword>\n")
                self.__token.advance()
            elif self.__token.token_type() == "IDENTIFIER":
                self.__output_lines.write(self.__indentation + "<identifier> " +
                                          self.__token.identifier() + " </identifier>\n")
                self.__token.advance()
            elif self.__token.token_type() == "SYMBOL":
                if self.__token.symbol() == ")":
                    break
                self.__output_lines.write(self.__indentation + "<symbol> " +
                                          self.__token.symbol().lower() + " </symbol>\n")
                self.__token.advance()
        self.__add_sub_indentation(False)
        self.__output_lines.write(self.__indentation + "</parameterList>\n")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.__output_lines.write(self.__indentation + "<varDec>\n")
        self.__add_sub_indentation(True)
        self.__output_lines.write(self.__indentation + "<keyword> " +
                                  self.__token.keyword().lower() + " </keyword>\n")
        self.__token.advance()
        if self.__token.token_type() == "KEYWORD":
            self.__output_lines.write(self.__indentation + "<keyword> " +
                                      self.__token.keyword().lower() + " </keyword>\n")
        else:
            self.__output_lines.write(self.__indentation + "<identifier> " +
                                      self.__token.identifier() + " </identifier>\n")
        self.__token.advance()
        self.__output_lines.write(self.__indentation + "<identifier> " +
                                  self.__token.identifier() + " </identifier>\n")
        self.__token.advance()
        while self.__token.symbol() == ",":
            self.__output_lines.write(self.__indentation + "<symbol> , </symbol>\n")
            self.__token.advance()
            self.__output_lines.write(self.__indentation + "<identifier> " +
                                      self.__token.identifier() + " </identifier>\n")
            self.__token.advance()
        self.__output_lines.write(self.__indentation + "<symbol> ; </symbol>\n")
        self.__token.advance()
        self.__add_sub_indentation(False)
        self.__output_lines.write(self.__indentation + "</varDec>\n")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing
        "{}".
        """
        self.__output_lines.write(self.__indentation + "<statements>\n")
        self.__add_sub_indentation(True)
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
        self.__add_sub_indentation(False)
        self.__output_lines.write(self.__indentation + "</statements>\n")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.__output_lines.write(self.__indentation + "<doStatement>\n")
        self.__add_sub_indentation(True)
        self.__output_lines.write(self.__indentation + "<keyword> do </keyword>\n")
        self.__token.advance()
        self.__output_lines.write(self.__indentation + "<identifier> " +
                                  self.__token.identifier() + " </identifier>\n")
        self.__token.advance()
        while self.__token.token_type() == "SYMBOL" and self.__token.symbol() == ".":
            self.__output_lines.write(self.__indentation + "<symbol> . </symbol>\n")
            self.__token.advance()
            self.__output_lines.write(self.__indentation + "<identifier> " +
                                      self.__token.identifier() + " </identifier>\n")
            self.__token.advance()
        self.__output_lines.write(self.__indentation + "<symbol> ( </symbol>\n")
        self.__token.advance()
        self.compile_expression_list()
        self.__output_lines.write(self.__indentation + "<symbol> ) </symbol>\n")
        self.__token.advance()
        self.__output_lines.write(self.__indentation + "<symbol> ; </symbol>\n")
        self.__token.advance()
        self.__add_sub_indentation(False)
        self.__output_lines.write(self.__indentation + "</doStatement>\n")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.__output_lines.write(self.__indentation + "<letStatement>\n")
        self.__add_sub_indentation(True)
        self.__output_lines.write(self.__indentation + "<keyword> let </keyword>\n")
        self.__token.advance()
        self.__output_lines.write(self.__indentation + "<identifier> " +
                                  self.__token.identifier() + " </identifier>\n")
        self.__token.advance()
        if self.__token.token_type() == "SYMBOL" and self.__token.symbol() == "[":
            self.__output_lines.write(self.__indentation + "<symbol> [ </symbol>\n")
            self.__token.advance()
            self.compile_expression()
            self.__output_lines.write(self.__indentation + "<symbol> ] </symbol>\n")
            self.__token.advance()
        self.__output_lines.write(self.__indentation + "<symbol> = </symbol>\n")
        self.__token.advance()
        self.compile_expression()
        self.__output_lines.write(self.__indentation + "<symbol> ; </symbol>\n")
        self.__token.advance()
        self.__add_sub_indentation(False)
        self.__output_lines.write(self.__indentation + "</letStatement>\n")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self.__output_lines.write(self.__indentation + "<whileStatement>\n")
        self.__add_sub_indentation(True)
        self.__output_lines.write(self.__indentation + "<keyword> while </keyword>\n")
        self.__token.advance()
        self.__output_lines.write(self.__indentation + "<symbol> ( </symbol>\n")
        self.__token.advance()
        self.compile_expression()
        self.__output_lines.write(self.__indentation + "<symbol> ) </symbol>\n")
        self.__token.advance()
        self.__output_lines.write(self.__indentation + "<symbol> { </symbol>\n")
        self.__token.advance()
        self.compile_statements()
        self.__output_lines.write(self.__indentation + "<symbol> } </symbol>\n")
        self.__token.advance()
        self.__add_sub_indentation(False)
        self.__output_lines.write(self.__indentation + "</whileStatement>\n")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.__output_lines.write(self.__indentation + "<returnStatement>\n")
        self.__add_sub_indentation(True)
        self.__output_lines.write(self.__indentation + "<keyword> return </keyword>\n")
        self.__token.advance()
        if not (self.__token.token_type() == "SYMBOL" and self.__token.symbol() == ";"):
            self.compile_expression()
        self.__output_lines.write(self.__indentation + "<symbol> ; </symbol>\n")
        self.__token.advance()
        self.__add_sub_indentation(False)
        self.__output_lines.write(self.__indentation + "</returnStatement>\n")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self.__output_lines.write(self.__indentation + "<ifStatement>\n")
        self.__add_sub_indentation(True)
        self.__output_lines.write(self.__indentation + "<keyword> if </keyword>\n")
        self.__token.advance()
        self.__output_lines.write(self.__indentation + "<symbol> ( </symbol>\n")
        self.__token.advance()
        self.compile_expression()
        self.__output_lines.write(self.__indentation + "<symbol> ) </symbol>\n")
        self.__token.advance()
        self.__output_lines.write(self.__indentation + "<symbol> { </symbol>\n")
        self.__token.advance()
        self.compile_statements()
        self.__output_lines.write(self.__indentation + "<symbol> } </symbol>\n")
        self.__token.advance()
        if self.__token.token_type() == "KEYWORD" and self.__token.keyword() == "ELSE":
            self.__output_lines.write(self.__indentation + "<keyword> else </keyword>\n")
            self.__token.advance()
            self.__output_lines.write(self.__indentation + "<symbol> { </symbol>\n")
            self.__token.advance()
            self.compile_statements()
            self.__output_lines.write(self.__indentation + "<symbol> } </symbol>\n")
            self.__token.advance()

        self.__add_sub_indentation(False)
        self.__output_lines.write(self.__indentation + "</ifStatement>\n")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        self.__output_lines.write(self.__indentation + "<expression>\n")
        self.__add_sub_indentation(True)
        self.compile_term()
        while self.__token.token_type() == "SYMBOL" and self.__token.symbol() in \
                ["&lt;", "&gt;", "&amp;", "+", "-", "*", "/", "|", "="]:
            self.__output_lines.write(self.__indentation + "<symbol> " + self.__token.symbol() + " </symbol>\n")
            self.__token.advance()
            self.compile_term()
        self.__add_sub_indentation(False)
        self.__output_lines.write(self.__indentation + "</expression>\n")

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
        self.__output_lines.write(self.__indentation + "<term>\n")
        self.__add_sub_indentation(True)
        if self.__token.token_type() == "STRING_CONST":
            self.__output_lines.write(self.__indentation + "<stringConstant> " +
                                      self.__token.string_val()[1:-1] + " </stringConstant>\n")
            self.__token.advance()
        elif self.__token.token_type() == "INT_CONST":
            self.__output_lines.write(self.__indentation + "<integerConstant> " +
                                      str(self.__token.int_val()) + " </integerConstant>\n")
            self.__token.advance()
        elif self.__token.token_type() == "KEYWORD":
            self.__output_lines.write(self.__indentation + "<keyword> " +
                                      self.__token.keyword().lower() + " </keyword>\n")
            self.__token.advance()
        elif self.__token.token_type() == "IDENTIFIER":
            a = self.__token.identifier()
            self.__output_lines.write(self.__indentation + "<identifier> " +
                                      self.__token.identifier() + " </identifier>\n")
            self.__token.advance()
            if self.__token.token_type() == "SYMBOL" and self.__token.symbol() == "[":
                self.__output_lines.write(self.__indentation + "<symbol> [ </symbol>\n")
                self.__token.advance()
                self.compile_expression()
                self.__output_lines.write(self.__indentation + "<symbol> ] </symbol>\n")
                self.__token.advance()
            elif self.__token.token_type() == "SYMBOL" and self.__token.symbol() == "(":
                self.__output_lines.write(self.__indentation + "<symbol> ( </symbol>\n")
                self.__token.advance()
                self.compile_expression_list()
                self.__output_lines.write(self.__indentation + "<symbol> ) </symbol>\n")
                self.__token.advance()
            elif self.__token.token_type() == "SYMBOL" and self.__token.symbol() == ".":
                self.__output_lines.write(self.__indentation + "<symbol> . </symbol>\n")
                self.__token.advance()
                self.__output_lines.write(self.__indentation + "<identifier> " +
                                          self.__token.identifier() + " </identifier>\n")
                self.__token.advance()
                self.__output_lines.write(self.__indentation + "<symbol> ( </symbol>\n")
                self.__token.advance()
                self.compile_expression_list()
                self.__output_lines.write(self.__indentation + "<symbol> ) </symbol>\n")
                self.__token.advance()
        elif self.__token.token_type() == "SYMBOL" and self.__token.symbol() == "(":
            self.__output_lines.write(self.__indentation + "<symbol> ( </symbol>\n")
            self.__token.advance()
            self.compile_expression()
            self.__output_lines.write(self.__indentation + "<symbol> ) </symbol>\n")
            self.__token.advance()
        elif self.__token.token_type() == "SYMBOL" and self.__token.symbol() in "~-":
            self.__output_lines.write(self.__indentation + "<symbol> " +
                                      self.__token.symbol() + " </symbol>\n")
            self.__token.advance()
            self.compile_term()

        self.__add_sub_indentation(False)
        self.__output_lines.write(self.__indentation + "</term>\n")
        #  unaryOp term

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self.__output_lines.write(self.__indentation + "<expressionList>\n")
        self.__add_sub_indentation(True)
        if not (self.__token.token_type() == "SYMBOL" and self.__token.symbol() == ")"):
            self.compile_expression()
        while not (self.__token.token_type() == "SYMBOL" and self.__token.symbol() == ")"):
            self.__output_lines.write(self.__indentation + "<symbol> , </symbol>\n")
            self.__token.advance()
            self.compile_expression()
        self.__add_sub_indentation(False)
        self.__output_lines.write(self.__indentation + "</expressionList>\n")
