REGRAS_TEMPERATURA = r"""
    
    definir_temperatura: "DEFINIR_TEMPERATURA" IDENTIFICADOR "PARA" NUMERO
    
    ler_temperatura: "LER_TEMPERATURA" IDENTIFICADOR
    
    alerta_temperatura: "ALERTA_TEMP" TEXTO
    
    comando_temperatura: definir_temperatura
                       | ler_temperatura
                       | alerta_temperatura
"""
