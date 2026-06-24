REGRAS_TEMPERATURA = r"""
    dispositivo_termostato: "DISPOSITIVO" IDENTIFICADOR ":" "TERMOSTATO"
    
    definir_temperatura: "DEFINIR_TEMPERATURA" IDENTIFICADOR "PARA" NUMERO
    
    ler_temperatura: "LER_TEMPERATURA" IDENTIFICADOR
    
    alerta_temperatura: "ALERTA" TEXTO
    
    condicional_temperatura: "SE" IDENTIFICADOR COMPARADOR NUMERO "ENTAO" comando_temperatura "SENAO" comando_temperatura "FIM"
    
    comando_temperatura: definir_temperatura
                       | ler_temperatura
                       | alerta_temperatura
                       | condicional_temperatura
"""
