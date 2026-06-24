REGRAS_ENERGIA = r"""
    dispositivo_medidor_energia: "DISPOSITIVO" IDENTIFICADOR ":" "MEDIDOR_ENERGIA"

    definir_limite_energia: "DEFINIR_LIMITE_ENERGIA" IDENTIFICADOR "PARA" NUMERO "KWH"

    registrar_consumo_energia: "REGISTRAR_CONSUMO_ENERGIA" IDENTIFICADOR "PARA" NUMERO "KWH"

    ler_consumo_energia: "LER_CONSUMO_ENERGIA" IDENTIFICADOR

    resetar_consumo_energia: "RESETAR_CONSUMO_ENERGIA" IDENTIFICADOR

    alerta_energia: "ALERTA_ENERGIA" TEXTO

    condicional_energia: "SE" IDENTIFICADOR COMPARADOR NUMERO "ENTAO" comando_energia "SENAO" comando_energia "FIM"

    comando_energia: definir_limite_energia
                   | registrar_consumo_energia
                   | ler_consumo_energia
                   | resetar_consumo_energia
                   | alerta_energia
                   | condicional_energia
"""