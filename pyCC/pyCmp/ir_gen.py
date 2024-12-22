"""
    ir_gen.py\n
    Added by DrkWithT\n
    Defines AST to IR converter.
"""

from enum import Enum, auto
from pyCC.pyCmp.parser import ParseResult
from pyCC.pyCmp.ast_visitor import ASTVisitor
import pyCC.pyCmp.ast_nodes as ast
import pyCC.pyCmp.ir_types as ir_types

class IRAddrs(Enum):
    A = auto()
    B = auto()
    C = auto()
    TEMP = auto()

class IREmitter(ASTVisitor):
    AddrUsageTable = dict[str, bool]

    addr_table: AddrUsageTable = None
    results: ir_types.StepList = None
    call_frames: list = None

    def __init__(self):
        self.addr_table = {}
        self.call_frames = []
        self.results = []

    def get_addr_count(self) -> int:
        return len(self.addr_table.keys())

    def visit_literal(self, node):
        pass

    def visit_unary(self, node):
        pass

    def visit_binary(self, node):
        pass

    def visit_call(self, node):
        pass

    def visit_variable_decl(self, node):
        pass

    def visit_block(self, node):
        pass

    def visit_function_decl(self, node):
        pass

    def visit_expr_stmt(self, node):
        pass

    def visit_if(self, node):
        pass

    def visit_return(self, node):
        pass
