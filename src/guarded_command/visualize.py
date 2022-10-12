from graphviz import Digraph
from .controlflowgraph import ControlFlowGraph
import os 

def visul_cfg(cfg: ControlFlowGraph, name:str, path: str = '.'):
    graph = Digraph(name=name, format='png')
    for node in cfg.nodes:
        graph.node(str(node), str(node))
    for edge in cfg.edges:
        # print(edge.text)
        graph.edge(str(edge.start), str(edge.dest),label= edge.text)
    graph.view()