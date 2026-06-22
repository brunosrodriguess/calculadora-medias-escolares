# Sistema de Fechamento de Média Semestral

Sistema desktop desenvolvido em Python com interface gráfica moderna utilizando CustomTkinter para gerenciamento acadêmico de notas.

O sistema permite realizar cálculos automáticos de média, com base nas notas e frequência, definição de status acadêmico e armazenamento do histórico em banco de dados SQL.

---

## Funcionalidades

- Registro de notas
- Definição de pesos das avaliações
- Cálculo automático da média final
- Verificação de frequência para aprovação
- Classificação automática do aluno:
  - APROVADO
  - EXAME
  - REPROVADO (POR FALTA)
- Histórico de alunos
- Armazenamento local com SQL
- Interface gráfica moderna e intuitiva

---

## Tecnologias Utilizadas

- Python
- CustomTkinter
- Tkinter
- SQLite

---

## Instalação

Clone o repositório:

```bash
git clone URL_DO_REPOSITORIO
```

Acesse a pasta do projeto:

```bash
cd sistema-fechamento-media
```

Instale as dependências:

```bash
pip install customtkinter
```

---

## Como Executar

Execute o arquivo principal:

```bash
python trabalho_algoritmos.py
```

---

## Funcionamento do Sistema

O sistema realiza o cálculo da média ponderada utilizando:

- P1
- P2
- T1
- T2

Cada avaliação possui um peso definido pelo usuário.

A média final é calculada automaticamente com base nos pesos informados.

Além disso, o sistema:

- verifica a frequência do aluno
- define o status acadêmico
- salva os dados automaticamente no banco de dados
- permite visualizar o histórico completo dos alunos

---

## Regras de Aprovação

| Média maior ou igual a 7 | APROVADO |
| Média menor que 7 | EXAME |
| Frequência menor que 75% | REPROVADO POR FALTA |

---

## Autor

Bruno de Souza Rodrigues
Cauã Gasparoto Nascimento
João Igor Alves Oroz Reis
Diego Constanzo Galvão
Ana Clara Fernandes Moliterno