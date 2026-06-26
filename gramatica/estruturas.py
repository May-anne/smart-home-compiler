REGRAS_ESTRUTURAS = r"""
    repetir: "REPETIR" NUMERO "VEZES" instrucao+ "FIM"

    cena: "CENA" TEXTO "{" instrucao+ "}"

    agendar: "AGENDAR" instrucao "AS" HORA
"""
