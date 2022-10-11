from __future__ import annotations
from lark import Lark, Tree, v_args
from typing import List, Dict
from lark.visitors import Interpreter

class Program:

    def __init__(self, code: str) -> None:
        self.code: str = code
        with open('./grammar.lark', 'r') as f:
            self.grammar = f.read()

    @classmethod
    def read_file(path: str) -> Program | None:
        with open(path, 'r') as f:
            code = f.read()
            return Program(code)
    
    def run(self, vars:Dict[str, int] = {}, arrs: Dict[str, List[int]]={}, channels:Dict[str, List[int]]={}) -> Memory:
        """
        Interpreter the whole program by AST
        """
        gc_parser = Lark(self.grammar, start='command')
        tree = gc_parser.parse(self.code)
        interpreter = GC_Interpreter()
        interpreter.memory.initialize(vars, arrs, channels)
        interpreter.visit(tree)
        return interpreter.memory

class GC_Interpreter(Interpreter):
    def __init__(self) -> None:
        self.memory = Memory()
        self.rval: int = 0

    def print(self, tree) -> None:
        print(self.visit(tree))

    @v_args(inline=True)
    def name(self, var):
        var = str(var)
        return self.memory.read_var(var)

    # def var(self, tree) -> int:
    #     print(1111111111111)
    #     print(tree, tree[0])
    #     return self.memory.read_var(str(tree[0]))

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

    def true(self, tree) -> bool:
        return True
    
    def false(self, tree) -> bool:
        return False
    
    @v_args(inline=True)
    def and_(self, left, right) -> bool:
        left = self.visit(left)
        right = self.visit(right)
        return left and right

    @v_args(inline=True)
    def or_(self, left, right) -> bool:
        left = self.visit(left)
        right = self.visit(right)
        return left or right
    
    @v_args(inline=True)
    def eq(self, left, right) -> bool:
        left = self.visit(left)
        right = self.visit(right)
        return left == right

    @v_args(inline=True)
    def ne(self, left, right) -> bool:
        left = self.visit(left)
        right = self.visit(right)
        return left != right

    @v_args(inline=True)
    def gt(self, left, right) -> bool:
        left = self.visit(left)
        right = self.visit(right)
        return left > right

    @v_args(inline=True)
    def ge(self, left, right) -> bool:
        left = self.visit(left)
        right = self.visit(right)
        return left >= right
    
    @v_args(inline=True)
    def lt(self, left, right) -> bool:
        left = self.visit(left)
        right = self.visit(right)
        assert type(left) == int
        assert type(right) == int
        return left < right

    @v_args(inline=True)
    def le(self, left, right) -> bool:
        left = self.visit(left)
        right = self.visit(right)
        return left <= right
        
    @v_args(inline=True)
    def not_(self, left) -> bool:
        left = self.visit(left)
        return not left 

    def if_(self, tree: Tree):
        tree = tree.children[0]
        match tree.data:
            # simple condition
            case 'cond':
                cond, command = tree.children[0], tree.children[1]
                if self.visit(cond):
                    self.visit(command)
            # multi condition
            case 'case':
                raise NotImplemented()
            case _:
                raise NotImplemented()    
 
    def while_(self, tree: Tree) -> bool:
        tree = tree.children[0]
        match tree.data:
            # simple condition
            case 'cond':
                cond, command = tree.children[0], tree.children[1]
                while self.visit(cond):
                    self.visit(command)
                # print(command)
            # multi condition
            case 'case':
                raise NotImplemented()
            case _:
                raise NotImplemented()    
 
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
    
    def initialize(self, vars:Dict[str, int] = {}, arrs: Dict[str, List[int]]={}, channels:Dict[str, List[int]]={}) -> None:
        self.vars = vars
        self.arrs = arrs
        self.channels = channels