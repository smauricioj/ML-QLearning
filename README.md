# ML-QLearning

## Objetivos do projeto

Repositório dos codigos desenvolvidos na disciplina de Aprendizagem de Máquina, no tópico de Aprendizagem por Reforço e QLearning

## O que está incluso?

### QL

Implementação de uma classe para execussão do algorítmo de QLearning. Inclui diversos metaparâmetros, como fator de desconto, taxa de aprendizagem variável e divisão de esforço *exploration*/*exploitation*. Requer implementação específica da representação de 'Estado' para garantir eficiência da tabela hash.

### Jogo2048

Exemplo de aplicação da classe QL na exploração das ações e estados de uma partida de 2048. Inclui a caracterização específica de 'Estado'.

## Estrutura do projeto

```text
ML-QLearning/
├── Python/
│   ├── Jogo2048/
│   │   ├── __init__.py
│   │   ├── Estado2048.py
│   │   └── QL2048.py
│   ├── QL/
│   │   ├── __init__.py
│   │   ├── Estado.py
│   │   ├── ParSA.py
│   │   └── QL.py
│   ├── requirements.txt
│   └── main.py
├── README.md
├── LICENSE.md
└── .gitignore
```