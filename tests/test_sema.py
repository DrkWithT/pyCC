"""
    test_sema.py\n
    Added by DrkWithT\n
    Unit tests semantic analyzer on 1 positive, 3 negative samples.
"""

import unittest
import pyCC.pyCmp.parser as par
import pyCC.pyCmp.semantics as sema

class SemAnalyzerTester(unittest.TestCase):
    def test_good_4(self):
        parser = par.Parser()
        checker = sema.SemanticChecker()

        with open('./c_samples/test_04.c') as src:
            parser.use_source(src.read())
            ok, ast = parser.parse_all()

            if not ok:
                print('Parsing failed for source 4!')
            
            self.assertTrue(ok)

            errors = checker.check_ast(ast)

            for sem_err in errors:
                print(f'Semantic Error:\nCulprit symbol: {sem_err[0]}\nScope of {sem_err[1]}\n{sem_err[2]}\n')

            self.assertTrue(len(errors) == 0)
    
    def test_bad_1(self):
        parser = par.Parser()
        checker = sema.SemanticChecker()

        with open('./c_samples/test_bad_01.c') as src:
            parser.use_source(src.read())
            ok, ast = parser.parse_all()

            if not ok:
                print('Parsing failed for bad source 1!')

            self.assertTrue(ok)

            errors = checker.check_ast(ast)

            for sem_err in errors:
                print(f'Semantic Error:\nCulprit symbol: {sem_err[0]}\nScope of {sem_err[1]}\n{sem_err[2]}\n')

            self.assertTrue(len(errors) == 0)

    def test_bad_2(self):
        parser = par.Parser()
        checker = sema.SemanticChecker()

        with open('./c_samples/test_bad_02.c') as src:
            parser.use_source(src.read())
            ok, ast = parser.parse_all()

            if not ok:
                print('Parsing failed for bad source 2!')

            self.assertTrue(ok)

            errors = checker.check_ast(ast)

            for sem_err in errors:
                print(f'Semantic Error:\nCulprit symbol: {sem_err[0]}\nScope of {sem_err[1]}\n{sem_err[2]}\n')

            self.assertTrue(len(errors) == 0)

    def test_bad_3(self):
        parser = par.Parser()
        checker = sema.SemanticChecker()

        with open('./c_samples/test_bad_03.c') as src:
            parser.use_source(src.read())
            ok, ast = parser.parse_all()

            if not ok:
                print('Parsing failed for bad source 3!')

            self.assertTrue(ok)

            errors = checker.check_ast(ast)

            for sem_err in errors:
                print(f'Semantic Error:\nCulprit symbol: {sem_err[0]}\nScope of {sem_err[1]}\n{sem_err[2]}\n')

            self.assertTrue(len(errors) == 0)

if __name__ == '__main__':
    unittest.main()
