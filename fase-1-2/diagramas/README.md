# Diagramas UML — Etapa 2

Grupo: João Pedro Recalcatti e Sidney Alves Junior
Caso 1 — Sistema de Gestão de Biblioteca Universitária

## Arquivos

| Arquivo | Diagrama | O que o professor exigia |
|---|---|---|
| `01-casos-de-uso.drawio` | Casos de Uso | mín. 6 casos de uso, 1 `<<include>>` e 1 `<<extend>>` |
| `02-classes.drawio` | Classes | mín. 6 classes, atributos, métodos, multiplicidades, herança e agregação/composição |
| `03-sequencia-registrar-devolucao.drawio` | Sequência | um caso de uso crítico |
| `04-atividades-realizar-emprestimo.drawio` | Atividades | fluxo de negócio com decisão e paralelismo |

`gerar_diagramas.py` é o script que gera os 4 arquivos. Se precisar mudar
alguma coisa, dá para editar o script e rodar `python gerar_diagramas.py`
de novo — mas também dá para editar direto no Draw.io e salvar por cima.

## Como abrir e exportar em PNG

1. Entrar em https://app.diagrams.net (ou abrir o Draw.io instalado).
2. `Arquivo > Abrir de > Dispositivo` e escolher o `.drawio`.
3. Ajustar o que quiser arrastando as caixas.
4. `Arquivo > Exportar como > PNG`.
   - Marcar **Recorte** (corta a margem em branco).
   - Zoom **200%** (fica legível na impressão).
   - Marcar **Incluir uma cópia do diagrama** (assim o PNG continua editável).

A entrega pede os diagramas em PNG ou PDF, então exportem os 4 e entreguem
os PNGs junto com os `.drawio`.

## Onde cada exigência está atendida

**Casos de uso**
- `<<include>>`: *Registrar Empréstimo* e *Renovar Empréstimo* incluem
  *Validar Situação do Leitor*. A mesma validação é reaproveitada nos dois,
  que é justamente para isso que o include serve (RN01 e RN06).
- `<<extend>>`: *Gerar Multa* estende *Registrar Devolução*. Só acontece se
  a devolução foi atrasada — comportamento condicional (RN03).
- Generalização de ator: *Coordenador* herda de *Bibliotecário*, ou seja,
  faz tudo que o bibliotecário faz e mais um pouco.

**Classes**
- Herança: `Usuario` (abstrata) → `Aluno` e `Bibliotecario`;
  `Bibliotecario` → `Coordenador`.
- Composição (losango preenchido): `Livro` ◆— `Exemplar`. Um exemplar não
  existe sem o livro.
- Agregação (losango vazado): `Livro` ◇— `Autor`. O autor continua existindo
  mesmo sem aquele livro.
- Multiplicidades em todas as associações.

**Sequência — Registrar Devolução**
Escolhido por ser o caso de uso que mais concentra regra de negócio, e
porque o cálculo de multa é o que vamos implementar na Etapa 3.
Usa `alt` (atrasado / em dia) e `opt` (existe reserva na fila).

**Atividades — Realizar Empréstimo**
- Paralelismo: `fork` e `join` em volta de *Verificar situação do aluno* e
  *Verificar disponibilidade do exemplar*, que são independentes.
- Decisão: o losango depois do join só libera se as duas passarem.

## Importante

Os arquivos `.drawio` são a **fonte da verdade**. O `gerar_diagramas.py` foi
só o ponto de partida — ele já está sincronizado com os ajustes manuais feitos
no Draw.io, mas se você editar de novo pelo Draw.io e depois rodar o script,
o script **sobrescreve** o seu ajuste. Na dúvida, edite direto no Draw.io e
ignore o script.

## Checagem de notação (feita em 09/09)

- Os 4 atores estão FORA da fronteira do sistema (ator é entidade externa).
- Todos os 16 casos de uso estão DENTRO da fronteira.
- A seta `<<include>>` aponta do caso base para o caso incluído.
- A seta `<<extend>>` aponta do caso que estende para o caso base.
