REGRAS_FECHADURA = r"""
dispositivo_fechadura: "DISPOSITIVO" IDENTIFICADOR ":" "FECHADURA"
comando_fechadura: trancar | destrancar | alerta | verificar_senha

trancar: "TRANCAR" IDENTIFICADOR
destrancar: "DESTRANCAR" IDENTIFICADOR "COM" "SENHA" STRING
alerta: "ALERTA"
verificar_senha: "SE" IDENTIFICADOR "==" STRING "ENTAO" destrancar "SENAO" alerta "FIM"
"""

