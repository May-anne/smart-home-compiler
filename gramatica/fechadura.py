REGRAS_FECHADURA = r"""

    informar_senha_fechadura: "INFORMAR_SENHA_FECHADURA" IDENTIFICADOR "COM" "SENHA" TEXTO

    trancar: "TRANCAR" IDENTIFICADOR

    destrancar: "DESTRANCAR" IDENTIFICADOR

    alerta: "ALERTA"

    comando_fechadura: trancar 
                    | destrancar 
                    | informar_senha_fechadura 
                    | alerta
"""