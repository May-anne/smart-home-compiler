from gerador.gerador import gerar_programa

declarados = {
    "fechadura1":  "FECHADURA",
    "termostato1": "TERMOSTATO",
    "dimmer1":     "DIMMER",
    "detector1":   "INTDETECTOR",
    "agua1":       "MEDIDOR_AGUA",
    "energia1":    "MEDIDOR_ENERGIA",
}

nos = [
    {"acao": "dispositivo", "nome": "fechadura1",  "tipo": "FECHADURA",       "campos": []},
    {"acao": "dispositivo", "nome": "termostato1", "tipo": "TERMOSTATO",      "campos": []},
    {"acao": "dispositivo", "nome": "dimmer1",     "tipo": "DIMMER",          "campos": []},
    {"acao": "dispositivo", "nome": "detector1",   "tipo": "INTDETECTOR",     "campos": []},
    {"acao": "dispositivo", "nome": "agua1",       "tipo": "MEDIDOR_AGUA",    "campos": []},
    {"acao": "dispositivo", "nome": "energia1",    "tipo": "MEDIDOR_ENERGIA", "campos": []},

    {"acao": "trancar",   "nome": "fechadura1"},
    {"acao": "destrancar","nome": "fechadura1", "led": "VERDE"},
    {"acao": "alerta",    "nome": "fechadura1", "led": "VERMELHO"},
    {"acao": "informar_senha_fechadura", "nome": "fechadura1", "senha": "1234"},


    {"acao": "definir_temperatura", "alvo": "termostato1", "valor": 22},
    {"acao": "ler_temperatura",     "alvo": "termostato1"},
    {"acao": "alerta_temperatura",  "alvo": "termostato1", "mensagem": "Temp alta"},


    {"acao": "definir_luminosidade", "alvo": "dimmer1", "valor": 75},
    {"acao": "ler_luminosidade",     "alvo": "dimmer1"},
    {"acao": "alerta_luminosidade",  "alvo": "dimmer1", "mensagem": "Luz baixa"},


    {"acao": "configurar_detector",       "alvo": "detector1", "timeout": 30, "codigo": "ABC123"},
    {"acao": "armar_detector",            "alvo": "detector1"},
    {"acao": "desarmar_detector",         "alvo": "detector1"},
    {"acao": "detectar_presenca",         "alvo": "detector1"},
    {"acao": "informar_senha",            "alvo": "detector1", "senha": "9999"},
    {"acao": "timeout_expirado",          "alvo": "detector1"},
    {"acao": "disparar_alarme",           "alvo": "detector1"},
    {"acao": "definir_hora_funcionamento","alvo": "detector1", "hora_inicio": "08:00", "hora_fim": "18:00"},

    {"acao": "definir_limite_energia",    "alvo": "energia1", "valor": 500},
    {"acao": "registrar_consumo_energia", "alvo": "energia1", "valor": 120},
    {"acao": "ler_consumo_energia",       "alvo": "energia1"},
    {"acao": "resetar_consumo_energia",   "alvo": "energia1"},
    {"acao": "alerta_energia",            "alvo": "energia1", "mensagem": "Limite proximo"},

    {"acao": "definir_limite_agua",    "alvo": "agua1", "valor": 300},
    {"acao": "registrar_consumo_agua", "alvo": "agua1", "valor": 80},
    {"acao": "ler_consumo_agua",       "alvo": "agua1"},
    {"acao": "resetar_consumo_agua",   "alvo": "agua1"},
    {"acao": "alerta_agua",            "alvo": "agua1", "mensagem": "Consumo alto"},


    {
        "acao": "condicional",
        "alvo": "termostato1",
        "comparador": ">",
        "valor": {"tipo": "numero", "valor": 30},
        "se": [
            {"acao": "alerta_temperatura", "alvo": "termostato1", "mensagem": "Muito quente"},
            {"acao": "definir_temperatura", "alvo": "termostato1", "valor": 20},
        ],
        "senao": [
            {"acao": "definir_temperatura", "alvo": "termostato1", "valor": 25},
        ],
    },

    {
        "acao": "condicional",
        "alvo": "energia1",
        "comparador": ">=",
        "valor": {"tipo": "numero", "valor": 400},
        "se": [
            {"acao": "alerta_energia", "alvo": "energia1", "mensagem": "Limite de energia proximo"},
        ],
        "senao": [
            {"acao": "ler_consumo_energia", "alvo": "energia1"},
        ],
    },
    
    {
        "acao": "condicional",
        "alvo": "fechadura1",
        "comparador": "==",
        "valor": {"tipo": "string", "valor": "fechado"},
        "se": [
            {"acao": "alerta", "nome": "fechadura1", "led": "VERMELHO"},
        ],
        "senao": [
            {"acao": "trancar", "nome": "fechadura1"},
        ],
    },
]


if __name__ == "__main__":
    try:
        codigo = gerar_programa(nos, declarados)
        print(codigo)
    except Exception as e:
        print(f"[ERRO] {e}")