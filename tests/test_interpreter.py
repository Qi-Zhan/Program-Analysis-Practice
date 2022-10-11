import unittest
import os
import sys

test_dir = os.path.dirname( __file__ )
module_dir = os.path.join(test_dir, '..')
sys.path.append(module_dir)
from src.guarded_command.guarded_command_inter import Program

class VariableTestCase(unittest.TestCase):
    def test_arith_simple(self):
        arith = """x := (1+1)*3/2-2%2"""
        program = Program(arith)
        res = program.run()
        self.assertEqual((1+1)*3/2-2%2, res.read_var('x'))

    def test_while(self):
        code = """y:=1;
            do x>0 & true -> y:=x*y;
                    x:=x-1
            od
            """
        program = Program(code)
        res = program.run({'x':5})
        self.assertEqual(120, res.read_var('y'))
        program = Program(code)
        res = program.run({'x':0})
        self.assertEqual(1, res.read_var('y'))
    
    def test_if(self):
        code = """y:=1;
            if x>0 & y<2 -> y:=x*y;
                    x:=x-1
            fi
            """
        program = Program(code)
        res = program.run({'x':-1})
        self.assertEqual(1, res.read_var('y'))
        self.assertEqual(-1, res.read_var('x'))
        program = Program(code)
        res = program.run({'x':100})
        self.assertEqual(100, res.read_var('y'))
        self.assertEqual(99, res.read_var('x'))

class ArrayTestCase(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()