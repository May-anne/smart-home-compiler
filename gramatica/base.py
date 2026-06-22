from gramatica.fechadura import REGRAS_FECHADURA

TOKENS_COMPARTILHADOS = r"""
IDENTIFICADOR: /[a-zA-Z_][a-zA-Z0-9_]*/
NUMERO: /[0-9]+/
STRING: ESCAPED_STRING

%import common.ESCAPED_STRING
%ignore /[ \t\r]+/
%ignore /\/\/[^\n]*/
"""

REGRA_START: r"""
?start: comando+
comando: comando_fechadura
        | [...]
"""

GRAMATICA_COMPLETA = (
    TOKENS_COMPARTILHADOS
    + REGRAS_FECHADURA
)