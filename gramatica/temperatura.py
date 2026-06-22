# gramatica/temperatura.py
#
# Define as regras gramaticais da DSL para o módulo de temperatura.
# Este arquivo é concatenado com os demais módulos em gramatica/base.py.
#
# Terminais usados (definidos em base.py):
#   IDENTIFICADOR, NUMERO, COMPARADOR, TEXTO
#
# Palavras-chave do módulo (literais anônimas do Lark):
#   DISPOSITIVO, TERMOSTATO, DEFINIR_TEMPERATURA, LER_TEMPERATURA,
#   PARA, SE, ENTAO, SENAO, FIM, ALERTA

REGRAS_TEMPERATURA = r"""
    // ─── Declaração de dispositivo ───────────────────────────────────────────
    // Exemplo de uso: DISPOSITIVO sala : TERMOSTATO
    dispositivo_termostato: "DISPOSITIVO" IDENTIFICADOR ":" "TERMOSTATO"

    // ─── Comandos de temperatura ──────────────────────────────────────────────
    // Define a temperatura de um cômodo para um valor numérico (graus Celsius)
    // Exemplo: DEFINIR_TEMPERATURA sala PARA 22
    definir_temperatura: "DEFINIR_TEMPERATURA" IDENTIFICADOR "PARA" NUMERO

    // Lê e exibe a temperatura atual de um cômodo
    // Exemplo: LER_TEMPERATURA sala
    ler_temperatura: "LER_TEMPERATURA" IDENTIFICADOR

    // Emite um alerta textual (para uso dentro de condicionais)
    // Exemplo: ALERTA "Temperatura elevada!"
    alerta_temperatura: "ALERTA" TEXTO

    // ─── Condicional de temperatura ───────────────────────────────────────────
    // Estrutura: SE <dispositivo> <op> <valor> ENTAO <cmd> SENAO <cmd> FIM
    // Exemplo:
    //   SE sala > 25 ENTAO
    //       DEFINIR_TEMPERATURA sala PARA 20
    //   SENAO
    //       ALERTA "Temperatura ok"
    //   FIM
    condicional_temperatura: "SE" IDENTIFICADOR COMPARADOR NUMERO "ENTAO" comando_temperatura "SENAO" comando_temperatura "FIM"

    // ─── Regra guarda-chuva ───────────────────────────────────────────────────
    // Um comando de temperatura pode ser qualquer uma das opções acima.
    // O parser escolhe a alternativa correta com base nos tokens da entrada.
    comando_temperatura: dispositivo_termostato
                       | definir_temperatura
                       | ler_temperatura
                       | alerta_temperatura
                       | condicional_temperatura
"""
