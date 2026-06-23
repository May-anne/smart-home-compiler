REGRAS_LUMINOSIDADE = r"""
    dispositivo_dimmer: "DISPOSITIVO" IDENTIFICADOR ":" "DIMMER"

    definir_luminosidade: "DEFINIR_LUMINOSIDADE" IDENTIFICADOR "PARA" NUMERO

    ler_luminosidade: "LER_LUMINOSIDADE" IDENTIFICADOR

    alerta_luminosidade: "ALERTA_LUZ" TEXTO

    condicional_luminosidade: "SE" IDENTIFICADOR COMPARADOR NUMERO "ENTAO" comando_luminosidade "SENAO" comando_luminosidade "FIM"
    
    comando_luminosidade: dispositivo_dimmer
                        | definir_luminosidade
                        | ler_luminosidade
                        | alerta_luminosidade
                        | condicional_luminosidade
"""
