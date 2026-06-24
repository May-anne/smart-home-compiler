import unittest

from lark import Lark, UnexpectedInput

from gramatica.base import GRAMATICA_COMPLETA
from semantica import semantica_base
from transformer import transformer


DEVICE_VALIDO = """
device detector {
    type intrusion_detector;
    int timeout_alarm;
    string passkey;
    string start_time;
    string end_time;
    bool person_detected;
}
"""


class IntrusionDetectorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = Lark(GRAMATICA_COMPLETA, start="start", parser="lalr")

    def analisar(self, fonte):
        ast = transformer(self.parser.parse(fonte))
        declarados = {}
        tipos_definidos = {}
        for node in ast:
            semantica_base(node, declarados, tipos_definidos)
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
        self.assertEqual(ast[0]["acao"], "declarar_device")
        self.assertTrue(all(node["tipo"] == "void" for node in ast))

    def test_rejeita_campo_ausente(self):
        fonte = DEVICE_VALIDO.replace("    bool person_detected;\n", "")
        with self.assertRaisesRegex(Exception, "person_detected"):
            self.analisar(fonte)

    def test_rejeita_campo_extra(self):
        fonte = DEVICE_VALIDO.replace(
            "    bool person_detected;\n",
            "    bool person_detected;\n    bool campo_extra;\n",
        )
        with self.assertRaisesRegex(Exception, "campo_extra"):
            self.analisar(fonte)

    def test_rejeita_tipo_de_campo_incorreto(self):
        fonte = DEVICE_VALIDO.replace(
            "    int timeout_alarm;", "    float timeout_alarm;"
        )
        with self.assertRaisesRegex(Exception, "timeout_alarm"):
            self.analisar(fonte)

    def test_rejeita_campo_duplicado(self):
        fonte = DEVICE_VALIDO.replace(
            "    bool person_detected;\n",
            "    bool person_detected;\n    bool person_detected;\n",
        )
        with self.assertRaisesRegex(Exception, "duplicado"):
            self.analisar(fonte)

    def test_rejeita_dispositivo_duplicado(self):
        with self.assertRaisesRegex(Exception, "já foi declarado"):
            self.analisar(DEVICE_VALIDO + DEVICE_VALIDO)

    def test_rejeita_acao_para_alvo_nao_declarado(self):
        with self.assertRaisesRegex(Exception, "não foi declarado"):
            self.analisar("ARMAR detector")

    def test_rejeita_acao_para_device_de_outro_tipo(self):
        fonte = """
device porta {
    type locker;
}
ARMAR porta
"""
        with self.assertRaisesRegex(Exception, "esperado é INTDETECTOR"):
            self.analisar(fonte)

    def test_rejeita_declaracao_antiga(self):
        with self.assertRaises(UnexpectedInput):
            self.parser.parse("DISPOSITIVO detector : INTDETECTOR")

    def test_preserva_validacoes_dos_comandos(self):
        with self.assertRaisesRegex(Exception, "maior que zero"):
            self.analisar(
                DEVICE_VALIDO
                + 'CONFIGURAR detector COM TIMEOUT 0 SEGUNDOS E CODIGO "1234"'
            )

        with self.assertRaisesRegex(Exception, "devem ser diferentes"):
            self.analisar(
                DEVICE_VALIDO
                + "DEFINIR_HORA_FUNCIONAMENTO detector DAS 08:00 AS 08:00"
            )


if __name__ == "__main__":
    unittest.main()
