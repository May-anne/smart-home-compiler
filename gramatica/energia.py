REGRAS_ENERGIA = r"""
    
    definir_limite_energia: "DEFINIR_LIMITE_ENERGIA" IDENTIFICADOR "PARA" NUMERO "KWH"

    registrar_consumo_energia: "REGISTRAR_CONSUMO_ENERGIA" IDENTIFICADOR "PARA" NUMERO "KWH"

    ler_consumo_energia: "LER_CONSUMO_ENERGIA" IDENTIFICADOR

    resetar_consumo_energia: "RESETAR_CONSUMO_ENERGIA" IDENTIFICADOR

    alerta_energia: "ALERTA_ENERGIA" TEXTO

    comando_energia: definir_limite_energia
                   | registrar_consumo_energia
                   | ler_consumo_energia
                   | resetar_consumo_energia
                   | alerta_energia
"""