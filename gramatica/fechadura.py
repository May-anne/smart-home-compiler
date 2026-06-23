REGRAS_FECHADURA = r"""
dispositivo_fechadura: "DISPOSITIVO" IDENTIFICADOR ":" "FECHADURA"
comando_fechadura: trancar | destrancar | alerta

trancar: "TRANCAR" IDENTIFICADOR
destrancar: "DESTRANCAR" IDENTIFICADOR "COM" "SENHA" STRING
alerta: "ALERTA"
"""

