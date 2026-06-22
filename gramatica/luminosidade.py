# gramatica/luminosidade.py
#
# Define as regras gramaticais da DSL para o módulo de luminosidade.
# Este arquivo é concatenado com os demais módulos em gramatica/base.py.
#
# Terminais usados (definidos em base.py):
#   IDENTIFICADOR, NUMERO, COMPARADOR, TEXTO
#
# Palavras-chave do módulo (literais anônimas do Lark):
#   DISPOSITIVO, DIMMER, DEFINIR_LUMINOSIDADE, LER_LUMINOSIDADE,
#   PARA, SE, ENTAO, SENAO, FIM, ALERTA_LUZ
#
# NOTA: O alerta de luminosidade usa "ALERTA_LUZ" (e não "ALERTA")
# para evitar ambiguidade gramatical com o alerta de temperatura.

REGRAS_LUMINOSIDADE = r"""
    // ─── Declaração de dispositivo ───────────────────────────────────────────
    // Exemplo de uso: DISPOSITIVO quarto : DIMMER
    dispositivo_dimmer: "DISPOSITIVO" IDENTIFICADOR ":" "DIMMER"

    // ─── Comandos de luminosidade ─────────────────────────────────────────────
    // Define a luminosidade de um cômodo (valor em porcentagem: 0 a 100)
    // Exemplo: DEFINIR_LUMINOSIDADE quarto PARA 70
    definir_luminosidade: "DEFINIR_LUMINOSIDADE" IDENTIFICADOR "PARA" NUMERO

    // Lê e exibe a luminosidade atual de um cômodo
    // Exemplo: LER_LUMINOSIDADE quarto
    ler_luminosidade: "LER_LUMINOSIDADE" IDENTIFICADOR

    // Emite um alerta textual de luminosidade
    // Exemplo: ALERTA_LUZ "Luz insuficiente!"
    alerta_luminosidade: "ALERTA_LUZ" TEXTO

    // ─── Condicional de luminosidade ──────────────────────────────────────────
    // Estrutura: SE <dispositivo> <op> <valor> ENTAO <cmd> SENAO <cmd> FIM
    // Exemplo:
    //   SE quarto < 30 ENTAO
    //       DEFINIR_LUMINOSIDADE quarto PARA 80
    //   SENAO
    //       ALERTA_LUZ "Luminosidade ok"
    //   FIM
    condicional_luminosidade: "SE" IDENTIFICADOR COMPARADOR NUMERO "ENTAO" comando_luminosidade "SENAO" comando_luminosidade "FIM"

    // ─── Regra guarda-chuva ───────────────────────────────────────────────────
    comando_luminosidade: dispositivo_dimmer
                        | definir_luminosidade
                        | ler_luminosidade
                        | alerta_luminosidade
                        | condicional_luminosidade
"""
