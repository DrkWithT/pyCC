"""
    semantics.py\n
    Added by DrkWithT\n
    Contains semantic analyzer for AST checks.\n
    TODO add lvalue-rvalue semantic checks!
"""

from enum import Enum, auto
from pyCC.pyCmp.ast_visitor import ASTVisitor
import pyCC.pyCmp.ast_nodes as nodes
import pyCC.pyCmp.lexer as lex

## Constants & Aliases ##

# NOTE categorizes undefined symbols!
BOGUS_SCOPE_ID = -1

# NOTE denotes global scope ID of a symbol!
GLOBAL_SCOPE_ID = 0

class SymbolRole(Enum):
    ROLE_VAR = auto()
    ROLE_FUNC = auto()
    ROLE_NONE = auto()

class SymbolNote:
    """
        Denotes annotated semantic info about a symbol:\n
        * global scope?
        * role i.e variable / function
        * data type
    """
    def __init__(self, in_global: bool, role: SymbolRole, data_type: nodes.DataType, extras):
        self.in_global = in_global
        self.role = role
        self.data_type = data_type
        self.extras = extras

ScopeObj = dict[str, SymbolNote]

class ScopeStore:
    """
        A utility class to track symbol scope information per function or global area:\n
        * separate global "scope"
        * regular function "scopes"
    """
    def __init__(self):
        # NOTE global scope stored externally from scope stack, slight lookup boost?
        self.globals: ScopeObj = {}

        # NOTE small stack of scopes
        self.others: list[ScopeObj] = []

    def at_global_scope(self) -> bool:
        return len(self.others) == 0

    def get_global_scope(self) -> ScopeObj:
        return self.globals

    def get_current_scope(self) -> ScopeObj:
        if len(self.others) == 0:
            return self.get_global_scope()

        return self.others[len(self.others) - 1]

    def create_new_scope(self):
        self.others.append(ScopeObj())

    def pop_current_scope(self):
        self.others.pop()

# represents (symbol, scope-name, message)
ErrorChunk = tuple[str, str, str]

# NOTE maps an AST op to support flag per (CHAR, INT, VOID)... use DataType.FOO.index()!
ALLOWED_DATA_OPS = {
    "OP_CALL": [False, False, False],
    "OP_NEG": [False, True, False],
    "OP_MULT": [False, True, False],
    "OP_DIV": [False, True, False],
    "OP_ADD": [False, True, False],
    "OP_SUB": [False, True, False],
    "OP_EQUALITY": [True, True, False],
    "OP_INEQUALITY": [True, True, False],
    "OP_LT": [True, True, False],
    "OP_LTE": [True, True, False],
    "OP_GT": [True, True, False],
    "OP_GTE": [True, True, False],
    "OP_LOGIC_AND": [True, True, False],
    "OP_LOGIC_OR": [True, True, False],
    "OP_ASSIGN": [True, True, False],
    "OP_NONE": [True, True, False]
}

## Semantic Analyzer ##
ExprInfo = tuple[str, nodes.DataType]

class SemanticChecker(ASTVisitor):
    def __init__(self):
        self.scopes = ScopeStore()
        self.current_scope_name: str = 'global'
        self.errors: list[ErrorChunk] = []

    def clear_errors(self):
        self.errors.clear()

    def check_ast(self, tops: list[nodes.Stmt]) -> list[ErrorChunk]:
        for stmt in tops:
            stmt.accept_visitor(self)

        return self.errors

    def visit_literal(self, node: nodes.Literal) -> ExprInfo:
        opt_token, opt_other = node.get_data()
        result_name = ''
        result_type = nodes.DataType.VOID

        if opt_token is not None:
            if opt_token[2].value == lex.TokenType.TYPENAME_VOID:
                self.errors.append((
                    f'{opt_token[0]}',
                    self.current_scope_name,
                    f'Invalid data type "void" for literal!'
                ))
            elif opt_token[2].value == lex.TokenType.IDENTIFIER:
                result_name = opt_token[0]
                name_info = self.scopes.get_current_scope().get(result_name)
                name_type = name_info.data_type if name_info is not None else nodes.DataType.VOID
                result_type = name_type

                if result_type == nodes.DataType.VOID:
                    self.errors.append((
                        opt_token[0],
                        self.current_scope_name,
                        f'Literals of type {name_type.name} or undefined are forbidden!'
                    ))
        else:
            # TODO handle arrays?
            pass

        return (result_name, result_type)

    def visit_unary(self, node: nodes.Unary) -> ExprInfo:
        inner_result: ExprInfo = node.get_inner().accept_visitor(self)

        expr_type = node.get_inner().deduce_early_type()        
        expr_op = node.get_op_type()

        if not ALLOWED_DATA_OPS.get(expr_op.name)[expr_type.value]:
            self.errors.append((
                '<expr>',
                self.current_scope_name,
                f'Invalid {expr_op.name} on {expr_type.name} value!'
            ))

        return inner_result

    def visit_binary(self, node: nodes.Binary) -> ExprInfo:
        lhs_result: ExprInfo = node.get_lhs().accept_visitor(self)
        rhs_result: ExprInfo = node.get_rhs().accept_visitor(self)
        bin_op = node.get_op_type()

        lhs_opt_name, lhs_type = lhs_result
        lhs_type = lhs_type if lhs_opt_name == '' else self.scopes.get_current_scope().get(lhs_opt_name).data_type

        rhs_opt_name, rhs_type = rhs_result
        rhs_type = rhs_type if rhs_opt_name == '' else self.scopes.get_current_scope().get(rhs_opt_name).data_type

        if not ALLOWED_DATA_OPS.get(bin_op.name)[lhs_type.value] or not ALLOWED_DATA_OPS.get(bin_op.name)[rhs_type.value]:
            self.errors.append((
                '<expr>',
                self.current_scope_name,
                f'Invalid types for basic operation of {bin_op.name}'
            ))
            return ('', nodes.DataType.VOID)

        if bin_op == nodes.OpType.OP_ASSIGN and (lhs_type == nodes.DataType.VOID or lhs_type == nodes.DataType.UNKNOWN or node.get_lhs().get_op_type() == nodes.OpType.OP_CALL or not lhs_opt_name):
            self.errors.append((
                '<bogus target> = <expr>',
                self.current_scope_name,
                f'Invalid assignment to invalid type or target object (value category checks TODO)!'
            ))
            return ('', nodes.DataType.VOID)

        if lhs_type == rhs_type:
            return ('', lhs_type)
        elif lhs_type == nodes.DataType.VOID or rhs_type == nodes.DataType.VOID:
            return ('', nodes.DataType.VOID)
        elif lhs_type == nodes.DataType.INT or rhs_type == nodes.DataType.INT: # NOTE promote partial char expr to int?
            return ('', nodes.DataType.INT)
        elif lhs_type == nodes.DataType.CHAR and rhs_type == nodes.DataType.CHAR:
            return ('', nodes.DataType.CHAR)

        return ('', nodes.DataType.VOID)

    def visit_call(self, node: nodes.Call) -> tuple[str, nodes.DataType]:
        pass # TODO 7

    def visit_variable_decl(self, node: nodes.Variable):
        var_name = node.get_name()
        var_type = node.get_type()
        var_rhs = node.get_rhs()

        rhs_name, rhs_type = var_rhs.accept_visitor(self)

        if var_type == rhs_type:
            if var_rhs.get_op_type() != nodes.OpType.OP_CALL:
                self.errors.append((
                    rhs_name,
                    self.current_scope_name,
                    f'Invalid use of function {rhs_name} returning {rhs_type.name}'
                ))
            else:
                self.scopes.get_current_scope()[var_name] = SymbolNote(self.scopes.at_global_scope(), SymbolRole.ROLE_VAR, var_type, None);
        elif var_type == nodes.DataType.INT:
            self.scopes.get_current_scope()[var_name] = SymbolNote(self.scopes.at_global_scope(), SymbolRole.ROLE_VAR, var_type, None);
        elif var_type == nodes.DataType.CHAR:
            self.scopes.get_current_scope()[var_name] = SymbolNote(self.scopes.at_global_scope(), SymbolRole.ROLE_VAR, var_type, None);
        else: # NOTE: handle invalid types in var. decls: VOID
            self.errors.append((
                '<expr>',
                self.current_scope_name,
                f'Invalid type "void" within variable declaration of {var_name}!'
            ))

    def visit_block(self, node: nodes.Block):
        stmts = node.get_stmts()

        for temp in stmts:
            temp.accept_visitor(self)

    def visit_function_decl(self, node: nodes.FunctionDecl):
        func_name = node.get_name()
        func_retype = node.get_type()
        func_arity = node.get_arity()
        func_param_v = node.get_params()

        # NOTE track arity and parameter vars. for this new function!
        self.scopes.get_current_scope()[func_name] = SymbolNote(self.scopes.at_global_scope(), SymbolRole.ROLE_FUNC, func_retype, {
            "arity": func_arity,
            "ptypes": [param[0] for param in func_param_v]
        })

        self.scopes.create_new_scope()
        self.current_scope_name = func_name

        node.get_body().accept_visitor(self)

        self.scopes.pop_current_scope()

    def visit_expr_stmt(self, node: nodes.ExprStmt):
        if self.scopes.at_global_scope():
            self.errors.append((
                '<expr-stmt>',
                self.current_scope_name,
                f'Invalid placement of expr-stmt!'
            ))
            return

        inner_expr = node.get_inner()
        inner_op = inner_expr.get_op_type()

        if inner_op == nodes.OpType.OP_CALL:
            # NOTE visit a call expr here!
            inner_expr.accept_visitor(self)
            return

        self.errors.append((
            '<expr-stmt>',
            self.current_scope_name,
            f'Temporary values are forbidden!'
        ))

    def visit_if(self, node: nodes.If):
        if self.scopes.at_global_scope():
            self.errors.append((
                '<if-else-stmt>',
                self.current_scope_name,
                f'Invalid placement of if/else!'
            ))
            return

        node.get_conditions().accept_visitor(self)
        node.get_if_body().accept_visitor(self)
        
        else_body_opt = node.get_alt_body()

        if else_body_opt is not None:
            else_body_opt.accept_visitor(self)

    def visit_return(self, node: nodes.Return):
        if self.scopes.at_global_scope():
            self.errors.append((
                'return <expr>;',
                self.current_scope_name,
                f'Invalid placement of return!'
            ))
            return

        result_name, result_type = node.get_result_expr().accept_visitor(self)

        # NOTE lookup current function's return type to check return semantics!
        parent_func_retype = self.scopes.get_global_scope().get(self.current_scope_name).data_type

        if parent_func_retype != result_type:
            self.errors.append((
                result_name or 'return <expr>;',
                self.current_scope_name,
                f'Invalid return from function yielding type {parent_func_retype.name}!'
            ))
