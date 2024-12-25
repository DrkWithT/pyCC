"""
    test_ir_gen.py\n
    Added by DrkWithT\n
    Unit testing for IR generator from AST.
"""

import unittest
import pyCC.pyCmp.parser as par
import pyCC.pyCmp.semantics as sem
import pyCC.pyCmp.ir_gen as irgen

class IRGenTester(unittest.TestCase):
    def test_good_1(self):
        parser = par.Parser()
        checker = sem.SemanticChecker()

        with open('./c_samples/test_01.c') as src:
            parser.use_source(src)
            ok, ast = parser.parse_all()

            self.assertTrue(ok)
            if not ok:
                print('Parse failed!')
                return
            
            errors = checker.check_ast(ast)

            for err in errors:
                print(f'Semantic Error:\nCulprit symbol: {err[0]}\nScope of {err[1]}\n{err[2]}\n')
            
            self.assertTrue(len(errors) == 0)
            if len(errors) > 0:
                print('Semantic validation failed!')
                return

            ir_result = irgen.IREmitter(checker.eject_semantic_info()).gen_ir_from_ast(ast)

            self.assertTrue(len(ir_result) > 0)

            print('Generated IR:\n')
            for step in ir_result:
                print(f'{step}\n')
