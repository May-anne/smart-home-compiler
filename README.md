# Smart Home Compiler

Compilador de uma linguagem de domínio específico (DSL) para automação residencial inteligente, desenvolvido para a disciplina de Compiladores do curso de Engenharia da Computação — UPE.

---

## Equipe

- Ana Karla Dias
- Arthur Carvalho
- Arthur Lima
- Mayanne Gomes

---

## Motivação

Configurar dispositivos de uma casa inteligente normalmente exige escrever código em linguagens de propósito geral (C++, Python, etc.), o que força o programador a lidar com detalhes de implementação irrelevantes para a automação em si: instanciar objetos, chamar métodos com nomes específicos de cada biblioteca, gerenciar estado de sensores manualmente.

O **Smart Home Compiler** propõe uma linguagem de domínio específico, escrita em português, que permite descrever o comportamento de dispositivos residenciais de forma direta e legível, sem conhecimento prévio de programação orientada a objetos. O compilador traduz esses programas para código C++ funcional, pronto para ser integrado a um sistema embarcado.

---

## Descrição da Linguagem

A linguagem tem extensão `.shc` (Smart Home Compiler). Os programas são escritos em português e descrevem dispositivos e as operações que devem ser realizadas sobre eles.

### Declaração de dispositivos

Todo dispositivo deve ser declarado antes de ser usado, informando seu nome e tipo. Campos extras podem ser adicionados para armazenar informações específicas.

```
device termostato1 { type TERMOSTATO; }
device detector1   { type INTDETECTOR; int timeout_alerta; bool person_detected; }
```

Tipos de dispositivos suportados:

| Tipo             | Descrição                        |
|------------------|----------------------------------|
| `TERMOSTATO`     | Controle de temperatura          |
| `DIMMER`         | Controle de luminosidade         |
| `FECHADURA`      | Tranca eletrônica com senha      |
| `INTDETECTOR`    | Detector de intrusão             |
| `MEDIDOR_ENERGIA`| Medição de consumo de energia    |
| `MEDIDOR_AGUA`   | Medição de consumo de água       |

### Comandos por dispositivo

**Termostato**
```
DEFINIR_TEMPERATURA termostato1 PARA 22
LER_TEMPERATURA termostato1
ALERTA_TEMP "Temperatura fora do limite"
```

**Dimmer**
```
DEFINIR_LUMINOSIDADE dimmer1 PARA 75
LER_LUMINOSIDADE dimmer1
ALERTA_LUZ "Luz muito baixa"
```

**Fechadura**
```
INFORMAR_SENHA_FECHADURA fechadura1 COM SENHA "1234"
TRANCAR fechadura1
DESTRANCAR fechadura1
ALERTA
```

**Detector de intrusao**
```
CONFIGURAR detector1 COM TIMEOUT 30 SEGUNDOS E CODIGO "ABC123"
ARMAR detector1
DESARMAR detector1
detector1 DETECTOU PRESENCA
INFORMAR_SENHA detector1 COM "9999"
TIMEOUT detector1 EXPIRADO
DISPARAR_ALARME detector1
DEFINIR_HORA_FUNCIONAMENTO detector1 DAS 08:00 AS 18:00
```

**Medidor de energia**
```
DEFINIR_LIMITE_ENERGIA energia1 PARA 500 KWH
REGISTRAR_CONSUMO_ENERGIA energia1 PARA 120 KWH
LER_CONSUMO_ENERGIA energia1
RESETAR_CONSUMO_ENERGIA energia1
ALERTA_ENERGIA "Limite proximo"
```

**Medidor de agua**
```
DEFINIR_LIMITE_AGUA agua1 PARA 300 LITROS
REGISTRAR_CONSUMO_AGUA agua1 PARA 80 LITROS
LER_CONSUMO_AGUA agua1
RESETAR_CONSUMO_AGUA agua1
ALERTA_AGUA "Consumo alto"
```

### Condicional

```
SE termostato1 > 30 ENTAO
    ALERTA_TEMP "Muito quente"
    DEFINIR_TEMPERATURA termostato1 PARA 20
SENAO
    DEFINIR_TEMPERATURA termostato1 PARA 25
FIM
```

Operadores de comparação suportados: `>`, `<`, `>=`, `<=`, `==`, `!=`

### Comentarios

```
// Isto é um comentário e será ignorado pelo compilador
```

---

## Pipeline do Compilador

O projeto implementa as quatro etapas clássicas de um compilador:

```
Código-fonte (.shc)
       |
       v
  Análise Léxica e Sintática  (Lark — parser LALR, gramática formal em EBNF)
       |
       v
  Transformação para AST       (Transformer orientado a sintaxe)
       |
       v
  Análise Semântica            (Verificação de tipos, declarações e restrições)
       |
       v
  Geração de Código            (Saída em C++)
```

---

## Como Executar

### Pré-requisitos

- Python 3.11 ou superior
- pip

### Instalação

```bash
pip install -r requirements.txt
```

### Execução

```bash
python main.py
```

Por padrão, o compilador processa o arquivo `exemplos/exemplo_valido.shc`. Para selecionar outro exemplo, edite a variável `EXEMPLO_ATIVO` no início de [main.py](main.py):

```python
# Opções: "valido", "erro_sintatico", "erro_semantico"
EXEMPLO_ATIVO = "valido"
```

### Executar os testes

```bash
pytest testes/
```

### Abrindo no GitHub Codespaces

O repositório inclui configuração `.devcontainer/devcontainer.json`. Ao abrir um Codespace, as dependências são instaladas automaticamente. Após o ambiente inicializar, basta executar:

```bash
python main.py
```

---

## Exemplos de Programas

### Programa valido

Arquivo: `exemplos/exemplo_valido.shc`

```
device fechadura1  { type FECHADURA; }
device termostato1 { type TERMOSTATO; }
device dimmer1     { type DIMMER; }
device detector1   { type INTDETECTOR; int timeout_alerta; string start_time; string end_time; bool person_detected; }
device agua1       { type MEDIDOR_AGUA; }
device energia1    { type MEDIDOR_ENERGIA; }

INFORMAR_SENHA_FECHADURA fechadura1 COM SENHA "1234"
DESTRANCAR fechadura1
ALERTA

DEFINIR_TEMPERATURA termostato1 PARA 22
LER_TEMPERATURA termostato1
ALERTA_TEMP "Temperatura muito alta"

DEFINIR_LUMINOSIDADE dimmer1 PARA 75
LER_LUMINOSIDADE dimmer1
ALERTA_LUZ "Luz baixa"

CONFIGURAR detector1 COM TIMEOUT 30 SEGUNDOS E CODIGO "ABC123"
ARMAR detector1
DESARMAR detector1
detector1 DETECTOU PRESENCA
INFORMAR_SENHA detector1 COM "9999"
TIMEOUT detector1 EXPIRADO
DISPARAR_ALARME detector1
DEFINIR_HORA_FUNCIONAMENTO detector1 DAS 08:00 AS 18:00

DEFINIR_LIMITE_ENERGIA energia1 PARA 500 KWH
REGISTRAR_CONSUMO_ENERGIA energia1 PARA 120 KWH
LER_CONSUMO_ENERGIA energia1
RESETAR_CONSUMO_ENERGIA energia1
ALERTA_ENERGIA "Limite proximo"

DEFINIR_LIMITE_AGUA agua1 PARA 300 LITROS
REGISTRAR_CONSUMO_AGUA agua1 PARA 80 LITROS
LER_CONSUMO_AGUA agua1
RESETAR_CONSUMO_AGUA agua1
ALERTA_AGUA "Consumo alto"

SE termostato1 > 30 ENTAO
    ALERTA_TEMP "Muito quente"
    DEFINIR_TEMPERATURA termostato1 PARA 20
SENAO
    DEFINIR_TEMPERATURA termostato1 PARA 25
FIM
```

Saída gerada (codigo C++):

```cpp
#include "SmartHome.h"
#include <iostream>

int main() {
    Fechadura fechadura1;
    Termostato termostato1;
    Dimmer dimmer1;
    IntDetector detector1;
    MedidorAgua agua1;
    MedidorEnergia energia1;
    fechadura1.setSenha("1234");
    fechadura1.destrancar();
    std::cout << "[ALERTA] Alerta de fechadura acionado" << std::endl;
    termostato1.setTemperatura(22);
    std::cout << "[TEMP] " << termostato1.getTemperatura() << std::endl;
    std::cout << "[TEMP] Temperatura muito alta" << std::endl;
    dimmer1.setLuminosidade(75);
    std::cout << "[LUZ] " << dimmer1.getLuminosidade() << std::endl;
    std::cout << "[LUZ] Luz baixa" << std::endl;
    detector1.configurar(30, "ABC123");
    detector1.armar();
    detector1.desarmar();
    detector1.detectarPresenca();
    detector1.informarSenha("9999");
    detector1.timeoutExpirado();
    detector1.dispararAlarme();
    detector1.setHorarioFuncionamento("08:00", "18:00");
    energia1.setLimite(500.0);
    energia1.registrarConsumo(120.0);
    std::cout << "[ENERGIA] " << energia1.getConsumo() << " kWh" << std::endl;
    energia1.resetarConsumo();
    std::cout << "[ENERGIA] Limite proximo" << std::endl;
    agua1.setLimite(300.0);
    agua1.registrarConsumo(80.0);
    std::cout << "[AGUA] " << agua1.getConsumo() << " L" << std::endl;
    agua1.resetarConsumo();
    std::cout << "[AGUA] Consumo alto" << std::endl;
    if (termostato1.getTemperatura() > 30) {
        std::cout << "[TEMP] Muito quente" << std::endl;
        termostato1.setTemperatura(20);
    } else {
        termostato1.setTemperatura(25);
    }
    return 0;
}
```

---

### Erro sintatico

Arquivo: `exemplos/exemplo_erro_sintatico.shc`

```
device termostato1 { type TERMOSTATO; }

// Erro sintático: falta a palavra PARA antes do valor.
DEFINIR_TEMPERATURA termostato1 22
```

O compilador rejeita o programa na fase de análise sintática antes de gerar qualquer código.

---

### Erro semantico

Arquivo: `exemplos/exemplo_erro_semantico.shc`

```
device dimmer1 { type DIMMER; }

// A sintaxe é válida, mas um DIMMER não pode receber um comando de temperatura.
DEFINIR_TEMPERATURA dimmer1 PARA 22
```

O programa passa pela análise sintática, mas é rejeitado na análise semântica: o compilador detecta que o dispositivo `dimmer1` é do tipo `DIMMER` e não aceita comandos de temperatura.
