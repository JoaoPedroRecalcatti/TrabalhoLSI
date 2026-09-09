# Sistema de Gestão de Biblioteca Universitária

Atividade Prática de **Laboratório de Sistemas de Informação** — UEMS
Curso de Sistemas de Informação · Professor France Ricardo

**Grupo:** João Pedro Recalcatti e Sidney Alves Junior
**Caso 1** — Sistema de Gestão de Biblioteca Universitária

A UEMS quer modernizar a biblioteca. O sistema permite reservas online,
renovações, controle de multas, integração com o sistema acadêmico para
bloqueio de alunos inadimplentes e relatórios para a coordenação, com perfis
distintos para aluno, bibliotecário e coordenador.

## Organização

| Pasta | Etapa | Conteúdo |
|---|---|---|
| [`fase-1/`](fase-1) | Levantamento de Requisitos | Documento com os atores, 14 requisitos funcionais, 10 regras de negócio e 8 requisitos não funcionais |
| [`fase-2/`](fase-2) | Modelagem UML | Os 4 diagramas (casos de uso, classes, sequência e atividades) e o documento que os explica |
| [`fase-3/`](fase-3) | Implementação do Protótipo | Protótipo funcional em Python + Flask + SQLite |

## O protótipo

Feito em Python com Flask e banco SQLite.

```bash
cd fase-3
pip install -r requirements.txt
python criar_banco.py
python app.py
```

Depois abrir <http://localhost:5000>.

### Contas para teste

| Perfil | E-mail | Senha |
|---|---|---|
| Bibliotecário | `maria@uems.br` | `123` |
| Aluno | `joao@uems.br` | `123` |

### O que o protótipo faz

- **Login com dois perfis** — bibliotecário e aluno veem menus e telas diferentes
- **Cadastro de livros (CRUD)** — criar, listar, editar e excluir, com persistência em banco
- **Consulta ao acervo com filtro** — por título ou autor, por categoria e por disponibilidade
- **Regra de negócio: cálculo da multa por atraso** — R$ 1,00 por dia (RN03), gerada
  automaticamente na devolução, com bloqueio do aluno inadimplente (RN06)

Os detalhes de cada tela e a ligação com os diagramas estão no
[README da fase 3](fase-3/README.md).
