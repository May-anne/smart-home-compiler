REGRAS_LUMINOSIDADE = r"""
    
    definir_luminosidade: "DEFINIR_LUMINOSIDADE" IDENTIFICADOR "PARA" NUMERO

    ler_luminosidade: "LER_LUMINOSIDADE" IDENTIFICADOR

    alerta_luminosidade: "ALERTA_LUZ" TEXTO
    
    comando_luminosidade: definir_luminosidade
                        | ler_luminosidade
                        | alerta_luminosidade
"""
