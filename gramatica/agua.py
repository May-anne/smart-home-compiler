REGRAS_AGUA = r"""
    dispositivo_medidor_agua: "DISPOSITIVO" IDENTIFICADOR ":" "MEDIDOR_AGUA"

    definir_limite_agua: "DEFINIR_LIMITE_AGUA" IDENTIFICADOR "PARA" NUMERO "LITROS"

    registrar_consumo_agua: "REGISTRAR_CONSUMO_AGUA" IDENTIFICADOR "PARA" NUMERO "LITROS"

    ler_consumo_agua: "LER_CONSUMO_AGUA" IDENTIFICADOR

    resetar_consumo_agua: "RESETAR_CONSUMO_AGUA" IDENTIFICADOR

    alerta_agua: "ALERTA_AGUA" TEXTO

    condicional_agua: "SE" IDENTIFICADOR COMPARADOR NUMERO "ENTAO" comando_agua "SENAO" comando_agua "FIM"

    comando_agua: definir_limite_agua
                | registrar_consumo_agua
                | ler_consumo_agua
                | resetar_consumo_agua
                | alerta_agua
                | condicional_agua
"""