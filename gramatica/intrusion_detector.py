REGRAS_INTRUSIONDETECTOR = r"""
    comando_intrusao: configurar_detector
                    | armar_detector
                    | desarmar_detector
                    | detectar_presenca
                    | informar_senha
                    | timeout_expirado
                    | disparar_alarme
                    | definir_hora_funcionamento

    configurar_detector: "CONFIGURAR" IDENTIFICADOR "COM" "TIMEOUT" NUMERO "SEGUNDOS" "E" "CODIGO" TEXTO

    armar_detector: "ARMAR" IDENTIFICADOR

    desarmar_detector: "DESARMAR" IDENTIFICADOR

    detectar_presenca: IDENTIFICADOR "DETECTOU" "PRESENCA"

    informar_senha: "INFORMAR_SENHA" IDENTIFICADOR "COM" TEXTO

    timeout_expirado: "TIMEOUT" IDENTIFICADOR "EXPIRADO"

    disparar_alarme: "DISPARAR_ALARME" IDENTIFICADOR

    definir_hora_funcionamento: "DEFINIR_HORA_FUNCIONAMENTO" IDENTIFICADOR "DAS" HORA "AS" HORA

    HORA: /(?:[01][0-9]|2[0-3]):[0-5][0-9]/
"""
