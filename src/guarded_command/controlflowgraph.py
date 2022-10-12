"""
         parser      construct
program -------> AST ---------> Program Graph
                                      |
                                      | analysis
                                      | 
                        SMT           |
analysis assignment <--------- Constraints      
"""
from __future__ import annotations
from errno import EDEADLK
from typing import List
from lark import Tree
from .guarded_command_inter import Program

class Node():
    def __init__(self, num: int) -> None:
        self.num = num
        self.inedges = []
        self.outedges = []

    def success_edge(self) -> List[Node]:
        return self.outedges

    def __repr__(self) -> str:
        return f"q{self.num}"

class StartNode(Node):
    def __init__(self) -> None:
        super().__init__(0)

    def __repr__(self) -> str:
        return 'Entry'


class FinalNode(Node):
    def __init__(self) -> None:
        super().__init__(-1)  # 

    def __repr__(self) -> str:
        return 'Exit'


class Edge():
    def __init__(self, start: Node, dest: Node, command: Tree, text:str = '') -> None:
        self.start = start
        self.dest = dest
        start.outedges.append(self)
        dest.inedges.append(self)
        self.command = command
        self.text = text

    def __repr__(self) -> str:
        return f"{str(self.start)} {self.text} -->  {str(self.dest)}"        

class CondEdge(Edge):
    pass

class ControlFlowGraph():
    def __init__(self, program:Program) -> None:
        self.tree = program.parse()
        self.progarm = program
        self.nodes: List[Node] = [StartNode(), FinalNode()]
        self.edges: List[Edge] = []
        self.num = 1
        self.make_edge(self.tree, self.nodes[0], self.nodes[1])
        assert self.num == len(self.nodes) - 1  # ensure every node created insert to [nodes]      
        
    def make_node(self) -> Node:
        node = Node(self.num)
        self.num += 1
        self.nodes.append(node)
        return node

    def make_edge(self, tree: Tree, start: Node, final: Node): 
        """make CFG edges by divide and conquer

        Args:
            tree (Tree): code to construct CFG
            start (Node): begin node for part of AST
            final (Node): final node for part of AST
        """
        if type(tree) != Tree:
            return
        # print(tree.data)
        match tree.data:
            case 'command':  # comand; command
                node = self.make_node()
                self.make_edge(tree.children[0], start, node)
                self.make_edge(tree.children[1], node, final)

            case 'while_':
                tree = tree.children[0]
                match tree.data:
                    # simple condition
                    case 'cond':
                        self.make_edge(tree, start, start)
                        cond = tree.children[0]
                        new_cond = Tree('not_', [cond])
                        # print(cond, new_cond)
                        # print(self.progarm.tree2code(new_cond))
                        self.make_edge(new_cond, start, final)

                    # multi condition
                    case 'case':
                        raise NotImplemented()

                    case _:
                        raise NotImplemented()

            case 'cond':
                node = self.make_node()
                cond, commamd = tree.children[0], tree.children[1]
                self.make_edge(cond, start, node)
                self.make_edge(commamd, node, final)

            case _:  # default to start -> tree -> final
                edge = Edge(start, final, tree, self.progarm.tree2code(tree))
                self.edges.append(edge)