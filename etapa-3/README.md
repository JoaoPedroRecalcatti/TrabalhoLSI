# Etapa 3 — Protótipo do Sistema de Gestão de Biblioteca

**Grupo:** João Pedro Recalcatti e Sidney Alves Junior
**Caso 1** — Sistema de Gestão de Biblioteca Universitária
**Entrega:** 19/10

Feito em Python com Flask e banco SQLite.

## Como rodar

```bash
pip install -r requirements.txt
python criar_banco.py
python app.py
```

Depois abrir <http://localhost:5000> no navegador.

O `criar_banco.py` só precisa ser rodado uma vez. Se rodar de novo, ele apaga
tudo e recria com os dados de exemplo.

### Contas para entrar

| Perfil | E-mail | Senha |
|---|---|---|
| Bibliotecário | `maria@uems.br` | `123` |
| Aluno | `joao@uems.br` | `123` |

## O que o professor pediu e onde está

| Exigência | Onde está |
|---|---|
| Tela de login com **dois perfis** | `templates/login.html` e a função `login()` em `app.py`. O bibliotecário e o aluno veem menus e telas diferentes. |
| Tela de **cadastro (CRUD)** | `templates/livros.html` e `livro_form.html`. Cadastra, edita, lista e exclui livros. Persistência em SQLite. |
| Tela de **listagem com filtro** | `templates/acervo.html`. Filtra por título/autor, por categoria e por "só disponíveis". |
| Uma **regra de negócio** | Cálculo da multa por atraso. Fica em `models.py`, nos métodos `dias_de_atraso()` e `calcular_multa()`, e é disparada na função `devolver()` em `app.py`. |

## A regra de negócio

Quando o bibliotecário clica em **Devolver**, o sistema:

1. Marca a data de devolução como hoje.
2. Vê se passou da data prevista.
3. Se passou, conta os dias de atraso e multiplica por R$ 1,00 (RN03).
4. Cria a multa e mostra na tela.

É o mesmo caminho do diagrama de sequência da Etapa 2. O banco já vem com um
empréstimo **5 dias atrasado**, de propósito, para dar para demonstrar isso na
apresentação sem precisar esperar uma semana.

Outras regras que também estão implementadas:

| Regra | O que faz | Onde |
|---|---|---|
| RN01 | Máximo de 3 livros por aluno | `app.py`, função `emprestimos()` |
| RN02 | Prazo de 7 dias | `models.py`, `calcular_data_prevista()` |
| RN03 | Multa de R$ 1,00 por dia | `models.py`, `calcular_multa()` |
| RN06 | Aluno com multa em aberto fica bloqueado | `models.py`, `tem_multa_em_aberto()` |
| RN08 | Só empresta se tiver exemplar livre | `models.py`, `tem_disponivel()` |
| RNF02 | Senha guardada criptografada | `models.py`, `definir_senha()` |
| RNF03 | Aluno não abre tela de bibliotecário | `app.py`, `precisa_bibliotecario()` |

## Arquivos

```
etapa-3/
├── app.py            → as rotas (as telas do sistema)
├── models.py         → as 4 tabelas e as regras de negócio
├── criar_banco.py    → cria o banco e põe os dados de exemplo
├── templates/        → as telas em HTML
├── static/estilo.css → o visual
└── biblioteca.db     → o banco (criado ao rodar criar_banco.py)
```

## Ligação com o diagrama de classes da Etapa 2

As 4 tabelas do `models.py` são as classes principais do diagrama:
`Usuario`, `Livro`, `Emprestimo` e `Multa`.

Duas simplificações feitas de propósito, para o protótipo não ficar grande
demais:

- No diagrama, `Usuario` é classe abstrata com `Aluno` e `Bibliotecario`
  herdando dela. No código isso virou o campo `perfil`, que é a forma comum de
  representar herança no banco quando as filhas não têm campos próprios.
- No diagrama, `Livro` e `Exemplar` são classes separadas. No código o
  exemplar virou o campo `qtd_exemplares` do livro, já que o protótipo não
  precisa controlar cada cópia individualmente.
