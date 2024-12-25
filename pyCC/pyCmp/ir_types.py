"""
    ir_types.py\n
    Added by DrkWithT\n
    Defines 3-address code IR types.
"""

from enum import Enum, auto

## Aliases and Types ##

class IRType(Enum):
    LABEL = auto()         # <name>:
    CMP = auto()           # Cmp <arg0> <arg1>
    JUMP = auto()          # Jump <name>
    ARGV_PUSH = auto()     # PushArg <arg>
    FUNC_CALL = auto()     # Call <name>
    ADDR_DECLARE = auto()  # <addr> = <expr>
    ADDR_ASSIGN = auto()   # <addr> = <addr> <op> <addr>
    LOAD_CONSTANT = auto()      # $<integral>

class IROp(Enum):
    CALL = auto()
    NEGATE = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    ADD = auto()
    SUBTRACT = auto()
    COMPARE_EQ = auto()
    COMPARE_NEQ = auto()
    COMPARE_LT = auto()
    COMPARE_LTE = auto()
    COMPARE_GT = auto()
    COMPARE_GTE = auto()
    SET_VALUE = auto()
    NOP = auto()

CMP_INVERSES = {
    "COMPARE_EQ": IROp.COMPARE_NEQ,
    "COMPARE_NEQ": IROp.COMPARE_EQ,
    "COMPARE_LT": IROp.COMPARE_GTE,
    "COMPARE_LTE": IROp.COMPARE_GT,
    "COMPARE_GT": IROp.COMPARE_LTE,
    "COMPARE_GTE": IROp.COMPARE_LT
}

DATATYPE_SIZES = {
    "CHAR": 1,
    "INT": 4,
    "VOID": 0,
    "UNKNOWN": 0
}

class IRStep:
    def get_ir_type(self) -> IRType:
        pass

StepList = list[IRStep]
