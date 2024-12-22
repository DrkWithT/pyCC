"""
    ir_types.py\n
    Added by DrkWithT\n
    Defines 3-address code IR types.
"""

from enum import Enum, auto

## Aliases and Types ##

class IRType(Enum):
    LABEL = auto()         # <name>:
    FRAME_STARTER = auto() # StartFrame <N>
    FRAME_ENDER = auto()   # EndFrame <N>
    ARGV_PUSH = auto()     # PushArg <arg>
    FUNC_CALL = auto()     # Call <arg>
    ADDR_DECLARE = auto()  # <addr> = <expr>
    ADDR_ASSIGN = auto()   # <addr> = <addr> <op> <addr>

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

IRStep = tuple[IRType, tuple[IROp, ...]]
StepList = list[IRStep]
