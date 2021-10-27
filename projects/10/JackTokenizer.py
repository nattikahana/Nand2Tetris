"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    """
    SYMBOLS = '{}()[].,;+-*/&|<>=~'
    COMMENT_LINE = "//"
    KEYWORD = ['class', 'constructor', 'function', 'method', 'field', 'static',
               'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this',
               'let', 'do', 'if', 'else', 'while', 'return']

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        self.__location = 0
        self.__cur_token = None
        self.__input_lines = input_stream.read()
        self.__input_lines = self.__sub_comments("//", "\n")  # delete one line comments
        self.__input_lines = self.__sub_comments("/*", "*/")  # delete multi line comments

        self.__input_lines = self.__input_lines.replace("\n", ' ').replace("\t", ' ')
        final = ""
        instr = False
        for i, char in enumerate(self.__input_lines):
            if char == '"':
                instr = not instr
            if char != " " or instr:
                final += char
            if not instr and char == " " and i + 1 < len(self.__input_lines) and self.__input_lines[i + 1] != " ":
                final += " "
        self.__input_lines = final

    def __sub_comments(self, beg, end):
        """Removes comments from beg to end"""
        input_lines = self.__input_lines
        while input_lines.find(beg) != -1:
            i = input_lines.find(beg) + input_lines[input_lines.find(beg):].find(end) + len(end)
            input_lines = input_lines[:input_lines.find(beg)] + input_lines[i:]
        return input_lines

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        return self.__location < len(self.__input_lines)

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token. 
        This method should be called if has_more_tokens() is true. 
        Initially there is no current token.
        """
        token = ""
        if self.__input_lines[self.__location] in self.SYMBOLS:
            token = self.__input_lines[self.__location]
        elif self.__input_lines[self.__location] == '"':
            end_str = self.__location + self.__input_lines[self.__location + 1:].find('"') + 2
            token = self.__input_lines[self.__location:end_str]
        else:
            for char in self.__input_lines[self.__location:]:
                if char in self.SYMBOLS + " ":
                    break
                token += char

        if self.__location + len(token) < len(self.__input_lines) and \
                self.__input_lines[self.__location + len(token)] == " ":
            self.__location += 1
        self.__location += len(token)

        self.__cur_token = token
        if not self.__cur_token:
            self.advance()

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        if self.__cur_token in self.SYMBOLS:
            return "SYMBOL"
        elif self.__cur_token in self.KEYWORD:
            return "KEYWORD"
        elif self.__cur_token.isnumeric():
            return "INT_CONST"
        elif self.__cur_token[0] == '"':
            return "STRING_CONST"
        return "IDENTIFIER"

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", 
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO", 
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        return self.__cur_token.upper()

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
        """
        special_chars = {"<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;"}
        if self.__cur_token in special_chars:
            return special_chars[self.__cur_token]
        return self.__cur_token

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
        """
        return self.__cur_token

    def int_val(self) -> int:
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
        """
        return self.__cur_token

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double 
            quotes. Should be called only when token_type() is "STRING_CONST".
        """
        return self.__cur_token
