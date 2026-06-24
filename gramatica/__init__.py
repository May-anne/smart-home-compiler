from gramatica.temperatura import REGRAS_TEMPERATURA
from gramatica.luminosidade import REGRAS_LUMINOSIDADE
from gramatica.fechadura import REGRAS_FECHADURA
from gramatica.intrusion_detector import REGRAS_INTRUSIONDETECTOR
from gramatica.energia import REGRAS_ENERGIA
from gramatica.agua import REGRAS_AGUA
from gramatica.device import REGRAS_DEVICE

TOKENS_COMPARTILHADOS = r"""
    IDENTIFICADOR: /[a-zA-Z_][a-zA-Z0-9_]*/
    NUMERO: /-?[0-9]+(?:\.[0-9]+)?/
    COMPARADOR: ">=" | "<=" | "==" | "!=" | ">" | "<"

    %import common.ESCAPED_STRING -> TEXTO
    %import common.WS
    %ignore WS
    COMENTARIO: /\/\/[^\n]*/
    %ignore COMENTARIO
"""

REGRA_START = r"""
    start: (device | instrucao)+
    instrucao: comando_temperatura
             | comando_luminosidade
             | comando_fechadura
             | comando_intrusao
             | comando_energia
             | comando_agua
             | condicional
    valor: TEXTO
           | NUMERO
    condicional: "SE" IDENTIFICADOR COMPARADOR valor "ENTAO" bloco "SENAO" bloco "FIM"
    bloco: instrucao+
"""

GRAMATICA_COMPLETA = (
    TOKENS_COMPARTILHADOS
    + REGRAS_DEVICE
    + REGRAS_TEMPERATURA
    + REGRAS_LUMINOSIDADE
    + REGRAS_FECHADURA
    + REGRAS_INTRUSIONDETECTOR
    + REGRAS_ENERGIA
    + REGRAS_AGUA
    + REGRAS_DEVICE
    + REGRA_START
)
