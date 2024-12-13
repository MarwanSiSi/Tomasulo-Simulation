from enum import Enum


class Opcode(Enum):
    DADDI = "DADDI"
    DSUBI = "DSUBI"
    ADD_D = "ADD.D"
    ADD_S = "ADD.S"
    SUB_D = "SUB.D"
    SUB_S = "SUB.S"
    MUL_D = "MUL.D"
    MUL_S = "MUL.S"
    DIV_D = "DIV.D"
    DIV_S = "DIV.S"
    LW = "LW"
    LD = "LD"
    L_S = "L.S"
    L_D = "L.D"
    SW = "SW"
    SD = "SD"
    S_S = "S.S"
    S_D = "S.D"
    BNE = "BNE"
    BEQ = "BEQ"
