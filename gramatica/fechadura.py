REGRAS_FECHADURA = r"""
dispositivo_fechadura: "DISPOSITIVO" IDENTIFICADOR ":" "FECHADURA"
comando_fechadura: trancar | destrancar | informar_senha_fechadura | alerta

informar_senha_fechadura: "INFORMAR_SENHA" IDENTIFICADOR "COM" "SENHA" TEXTO
trancar: "TRANCAR" IDENTIFICADOR
destrancar: "DESTRANCAR" IDENTIFICADOR
alerta: "ALERTA"
"""