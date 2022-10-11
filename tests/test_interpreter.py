import unittest
import os
import sys

test_dir = os.path.dirname( __file__ )
module_dir = os.path.join(test_dir, '..')
# module_dir = os.path.join(test_dir, '..', 'src', 'parser')
sys.path.append(module_dir)
from src.parser.guarded_command_parser import Program

class InterpreterTestCase(unittest.TestCase):
    def test_arith_simple(self):
        arith = """x := (1+1)*3/2-2%2"""
        program = Program(arith)
        program.run()
        self.assertEqual((1+1)*3/2-2%2, program.memory.read_var('x'))

if __name__ == '__main__':
    unittest.main()