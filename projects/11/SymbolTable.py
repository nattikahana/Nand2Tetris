"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
# import typing


class SymbolTable:
    """A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """

    def __init__(self) -> None:
        """Creates a new empty symbol table."""
        self.__class_table = dict()
        self.__subroutine_table = dict()
        self.__field_index = 0
        self.__static_index = 0
        self.__local_index = 0
        self.__argument_index = 0

    def start_subroutine(self) -> None:
        """Starts a new subroutine scope (i.e., resets the subroutine's 
        symbol table).
        """
        self.__subroutine_table = dict()
        self.__local_index = 0
        self.__argument_index = 0

    def define(self, name: str, type_: str, kind: str) -> None:
        """Defines a new identifier of a given name, type and kind and assigns 
        it a running index. "STATIC" and "FIELD" identifiers have a class scope, 
        while "ARG" and "VAR" identifiers have a subroutine scope.

        Args:
            name (str): the name of the new identifier.
            type_ (str): the type of the new identifier.
            kind (str): the kind of the new identifier, can be:
            "STATIC", "FIELD", "ARG", "VAR".
        """
        if kind == "STATIC":
            self.__class_table[name] = (type_, kind, self.__static_index)
            self.__static_index += 1
        elif kind == "FIELD":
            self.__class_table[name] = (type_, kind, self.__field_index)
            self.__field_index += 1
        elif kind == "ARG":
            self.__subroutine_table[name] = (type_, kind, self.__argument_index)
            self.__argument_index += 1
        elif kind == "VAR":
            self.__subroutine_table[name] = (type_, kind, self.__local_index)
            self.__local_index += 1

    def var_count(self, kind: str) -> int:
        """
        Args:
            kind (str): can be "STATIC", "FIELD", "ARG", "VAR".

        Returns:
            int: the number of variables of the given kind already defined in 
            the current scope.
        """
        dict_ = dict()
        if kind in ["FIELD", "STATIC"]:
            dict_ = self.__class_table
        elif kind in ["ARG", "VAR"]:
            dict_ = self.__subroutine_table
        counter = 0
        # if len(dict_) == 0:
        #     return 0
        for i in tuple(dict_.values()):
            if kind == i[1]:
                counter += 1
        return counter

    def kind_of(self, name: str) -> str:
        """
        Args:
            name (str): name of an identifier.

        Returns:
            str: the kind of the named identifier in the current scope, or None
            if the identifier is unknown in the current scope.
        """
        if name in self.__subroutine_table:
            return self.__subroutine_table[name][1]
        elif name in self.__class_table:
            return self.__class_table[name][1]

    def type_of(self, name: str) -> str:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        if name in self.__subroutine_table:
            return self.__subroutine_table[name][0]
        elif name in self.__class_table:
            return self.__class_table[name][0]

    def index_of(self, name: str) -> int:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """
        if name in self.__subroutine_table:
            return self.__subroutine_table[name][2]
        elif name in self.__class_table:
            return self.__class_table[name][2]
