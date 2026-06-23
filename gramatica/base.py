from gramatica.temperatura import REGRAS_TEMPERATURA
from gramatica.luminosidade import REGRAS_LUMINOSIDADE
from gramatica.fechadura import REGRAS_FECHADURA

TOKENS_COMPARTILHADOS = r"""
    IDENTIFICADOR: /[a-z_][a-z0-9_]*/
    NUMERO: /-?[0-9]+(?:\.[0-9]+)?/
    COMPARADOR: ">=" | "<=" | "==" | "!=" | ">" | "<"

    %import common.ESCAPED_STRING -> TEXTO
    %import common.WS
    %ignore WS
    COMENTARIO: /\/\/[^\n]*/
    %ignore COMENTARIO
"""

REGRA_START = r"""
    start: instrucao+
    instrucao: comando_temperatura
             | comando_luminosidade
             | comando_fechadura
    valor: STRING
           | NUMERO
    condicional: "SE" IDENTIFICADOR COMPARADOR valor "ENTAO" bloco "SENAO" bloco "FIM"
    bloco: comando+

"""

GRAMATICA_COMPLETA = (
    TOKENS_COMPARTILHADOS
    + REGRAS_TEMPERATURA
    + REGRAS_LUMINOSIDADE
    + REGRAS_FECHADURA
    + REGRA_START
)