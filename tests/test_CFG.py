import unittest
import os
import sys
test_dir = os.path.dirname( __file__ )
module_dir = os.path.join(test_dir, '..')
sys.path.append(module_dir)

from src.guarded_command.controlflowgraph import ControlFlowGraph
from src.guarded_command.guarded_command_inter import Program
from src.guarded_command.visualize import visul_cfg

class CFGTestCase(unittest.TestCase):
    def read_code(self, file):
        path = os.path.join(test_dir, 'src', file)
        with open(path, 'r') as f:
            text = f.read()
        return text

    def test_simple(self):
        program = Program(self.read_code('factorial.gc'))
        cfg = ControlFlowGraph(program)
        # print('Nodes', cfg.nodes)
        # print('Edge', cfg.edges)
        self.assertEqual(5, len(cfg.nodes))
        self.assertEqual(5, len(cfg.edges))
        # visul_cfg(cfg, test_dir)
        

if __name__ == '__main__':
    unittest.main()