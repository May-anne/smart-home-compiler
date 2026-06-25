import unittest

from lark import Lark, UnexpectedInput

from gramatica import GRAMATICA_COMPLETA
from semantica import semantica_base
from transformer import transformer


DEVICE_VALIDO = """
device detector {
    type INTDETECTOR;
    int timeout_config;
    string codigo_acesso;
    bool presenca_detectada;
}
"""


class IntrusionDetectorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = Lark(GRAMATICA_COMPLETA, start="start", parser="lalr")

    def analisar(self, fonte):
        ast = transformer(self.parser.parse(fonte))
        declarados = {}
        senha_validada = {}
        for node in ast:
            semantica_base(node, declarados, senha_validada)
        return ast, declarados

    def test_declaracao_configuracao_horario_e_acoes(self):
        fonte = DEVICE_VALIDO + """
            CONFIGURAR detector COM TIMEOUT 30 SEGUNDOS E CODIGO "1234"
            DEFINIR_HORA_FUNCIONAMENTO detector DAS 08:00 AS 22:00
            ARMAR detector
            detector DETECTOU PRESENCA
            TIMEOUT detector EXPIRADO
            DISPARAR_ALARME detector
            INFORMAR_SENHA detector COM "1234"
            DESARMAR detector
        """
        ast, declarados = self.analisar(fonte)

        self.assertEqual(declarados["detector"], "INTDETECTOR")
        self.assertEqual(ast[0]["acao"], "dispositivo")
        self.assertTrue(all(node["tipo"] == "void" for node in ast))

    def test_declaracao_sem_campos_extra(self):
        ast, declarados = self.analisar(
            "device d { type INTDETECTOR; }\nARMAR d"
        )
        self.assertEqual(declarados["d"], "INTDETECTOR")

    #Horário de funcionamento (incluindo overnight)

    def test_horario_diurno(self):
        ast, _ = self.analisar(
            DEVICE_VALIDO + "DEFINIR_HORA_FUNCIONAMENTO detector DAS 08:00 AS 18:00"
        )
        node = ast[-1]
        self.assertEqual(node["hora_inicio"], "08:00")
        self.assertEqual(node["hora_fim"], "18:00")
        self.assertFalse(node["overnight"])

    def test_horario_overnight(self):
        """22:00 às 06:00 cruza a meia-noite — overnight deve ser True."""
        ast, _ = self.analisar(
            DEVICE_VALIDO + "DEFINIR_HORA_FUNCIONAMENTO detector DAS 22:00 AS 06:00"
        )
        node = ast[-1]
        self.assertEqual(node["hora_inicio"], "22:00")
        self.assertEqual(node["hora_fim"], "06:00")
        self.assertTrue(node["overnight"])

    def test_horario_overnight_fronteira_meia_noite(self):
        """23:30 às 00:30 é o caso-limite de overnight."""
        ast, _ = self.analisar(
            DEVICE_VALIDO + "DEFINIR_HORA_FUNCIONAMENTO detector DAS 23:30 AS 00:30"
        )
        self.assertTrue(ast[-1]["overnight"])

    def test_horario_overnight_ate_hora_exata(self):
        """21:00 às 09:00 — overnight longo."""
        ast, _ = self.analisar(
            DEVICE_VALIDO + "DEFINIR_HORA_FUNCIONAMENTO detector DAS 21:00 AS 09:00"
        )
        self.assertTrue(ast[-1]["overnight"])

    def test_rejeita_horario_igual(self):
        with self.assertRaisesRegex(Exception, "devem ser diferentes"):
            self.analisar(
                DEVICE_VALIDO
                + "DEFINIR_HORA_FUNCIONAMENTO detector DAS 08:00 AS 08:00"
            )

    #Validações de campos do device
    def test_rejeita_campo_duplicado(self):
        fonte = DEVICE_VALIDO.replace(
            "    bool presenca_detectada;\n",
            "    bool presenca_detectada;\n    bool presenca_detectada;\n",
        )
        with self.assertRaisesRegex(Exception, "duplicado"):
            self.analisar(fonte)

    def test_rejeita_dispositivo_duplicado(self):
        with self.assertRaisesRegex(Exception, "já foi declarado"):
            self.analisar(DEVICE_VALIDO + DEVICE_VALIDO)

    #Validações de acesso a dispositivo

    def test_rejeita_acao_para_alvo_nao_declarado(self):
        with self.assertRaisesRegex(Exception, "não foi declarado"):
            self.analisar("ARMAR detector")

    def test_rejeita_acao_para_device_de_outro_tipo(self):
        fonte = """
            device porta {
                type FECHADURA;
            }
            ARMAR porta
        """
        with self.assertRaisesRegex(Exception, "INTDETECTOR"):
            self.analisar(fonte)

    #Validações dos comandos

    def test_rejeita_timeout_zero(self):
        with self.assertRaisesRegex(Exception, "maior que zero"):
            self.analisar(
                DEVICE_VALIDO
                + 'CONFIGURAR detector COM TIMEOUT 0 SEGUNDOS E CODIGO "1234"'
            )

    def test_rejeita_timeout_negativo(self):
        with self.assertRaisesRegex(Exception, "maior que zero"):
            self.analisar(
                DEVICE_VALIDO
                + 'CONFIGURAR detector COM TIMEOUT -5 SEGUNDOS E CODIGO "1234"'
            )

    def test_rejeita_senha_vazia(self):
        with self.assertRaisesRegex(Exception, "não pode ser vazia"):
            self.analisar(DEVICE_VALIDO + 'INFORMAR_SENHA detector COM ""')

    def test_configurar_com_timeout_valido(self):
        ast, _ = self.analisar(
            DEVICE_VALIDO + 'CONFIGURAR detector COM TIMEOUT 60 SEGUNDOS E CODIGO "9999"'
        )
        node = ast[-1]
        self.assertEqual(node["timeout"], 60)
        self.assertEqual(node["codigo"], "9999")

    def test_todos_comandos_retornam_void(self):
        fonte = DEVICE_VALIDO + """
            CONFIGURAR detector COM TIMEOUT 10 SEGUNDOS E CODIGO "0000"
            ARMAR detector
            INFORMAR_SENHA detector COM "0000"
            detector DETECTOU PRESENCA
            TIMEOUT detector EXPIRADO
            DISPARAR_ALARME detector
            DESARMAR detector
        """
        ast, _ = self.analisar(fonte)
        for node in ast:
            self.assertEqual(node["tipo"], "void")


if __name__ == "__main__":
    unittest.main()
