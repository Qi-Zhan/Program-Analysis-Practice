from __future__ import annotations
from lark import Lark, Transformer, Tree, v_args
from typing import List
from lark.visitors import Interpreter

grammar = r"""
    ?command: var ":=" a                -> assign_var
        | arr "[" a "]" ":=" a          -> assign_arr
        | "read" var                    -> read_var
        | "read" arr "[" a "]"          -> read_arr
        | "write" a                     -> write
        | "skip"                        -> skip
        | command ";" command     
        | "if" gc "fi"                  -> if
        | "do" gc "od"                  -> while
        | "continue"                    -> continue
        | "break"                       -> break
        | "try" command "catch" hc "yrt"
        | "throw" exp
        | "print" a                     -> print

    ?gc: b "->" command 
        | gc "[]" gc
    
    ?hc: exp ":" command 
        | hc "[]" hc

    ?a : term
        | a "+" term    -> add
        | a "-" term    -> sub

    ?term : item
        | term "*" item -> mul
        | term "/" item -> div
        | term "%" item -> modulo

    ?item : NUMBER         -> num
        | var
        | arr"[" a "]"
        | "-" item         -> neg
        | "(" a  ")"    

    ?b : "true"         -> true
        | "false"       -> false
        | b "&" b       -> and
        | b "|" b       -> or
        | b "&&" b
        | b "||" b
        | "!" b         -> not
        | a "=" a       -> eq
        | a "!=" a      -> ne
        | a ">" a       -> gt
        | a ">=" a      -> ge
        | a "<" a       -> lt
        | a "<=" a      -> le
        | "(" b ")"     


    ?arr:NAME           -> name

    ?var:NAME           -> name

    ?exp:NAME           -> name

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS
    %ignore WS
"""


text1 = """y:=1;
do x>0 -> y:=x*y;
          x:=x-1
od
"""


class Program:

    def __init__(self, code: str) -> None:
        self.code: str = code

    @classmethod
    def read_file(path: str) -> Program | None:
        with open(path, 'r') as f:
            code = f.read()
            return Program(code)

    def run(self):
        """
        Interpreter the whole program by AST
        """
        gc_parser = Lark(grammar, start='command')
        tree = gc_parser.parse(self.code)
        interpreter = GC_Interpreter()
        interpreter.visit(tree)
        self.memory = interpreter.memory

class GC_Interpreter(Interpreter):
    def __init__(self) -> None:
        self.memory = Memory()
        self.rval: int = 0

    def print(self, tree) -> None:
        print(self.memory.read_var('x'))

    def var(self, tree) -> str:
        return self.memory.read_var(tree[0])

    @v_args(inline=True)
    def assign_var(self, var, value) -> None:
        var = str(var.children[0])
        value = self.visit(value)
        assert type(value) == int
        self.memory.update_var(var, value)

    @v_args(inline=True)
    def add(self, left, right) -> int:
        left = self.visit(left)
        right = self.visit(right)
        return left + right

    @v_args(inline=True)
    def sub(self, left, right) -> int:
        left = self.visit(left)
        right = self.visit(right)
        return left - right

    @v_args(inline=True)
    def mul(self, left, right) -> int:
        left = self.visit(left)
        right = self.visit(right)
        return left * right

    @v_args(inline=True)
    def div(self, left, right) -> int:
        left = self.visit(left)
        right = self.visit(right)
        return int(left / right)

    @v_args(inline=True)
    def modulo(self, left, right) -> int:
        left = self.visit(left)
        right = self.visit(right)
        return left % right

    @v_args(inline=True)
    def neg(self, left) -> int:
        left = self.visit(left)
        return -left

    @v_args(inline=True)
    def add(self, left, right) -> int:
        left = self.visit(left)
        right = self.visit(right)
        return left + right


    def num(self, tree: Tree):
        assert tree.data == "num"
        return int(tree.children[0])

    def __default__(self, tree: Tree):
        self.visit_children(tree)


class Memory:
    def __init__(self):
        """Memory consists of three elements:
        * vars: map str -> value
        * arrs: map str -> value*
        * channels: map in/out -> value*
        """
        self.vars: dict[str, int] = {}
        self.arrs: dict[str, List] = {}
        self.channels: dict[str, List] = {"in": [], "out": []}

    def update_var(self, s: str, value: int) -> bool:
        self.vars[s] = value
        return False
    
    def read_var(self, s: str):
        return self.vars[s]
    
arith = """x := (1+1)*3/2-2%2; print x"""


gc_parser = Lark(grammar, start='command')
tree = gc_parser.parse(arith)
# print(tree.pretty())
# print((1+1)*3//2-2%2)
GC_Interpreter().visit(tree)