# Documento de Requisitos

**Disciplina:** Laboratório de Sistemas de Informação
**Professor:** France Ricardo
**Curso:** Sistemas de Informação — UEMS

**Grupo:** João Pedro Recalcatti e Sidney Alves Junior
**Caso:** 1 — Sistema de Gestão de Biblioteca Universitária

---

## 1. Sobre o sistema

A UEMS quer modernizar a biblioteca dela. Hoje muita coisa é feita no balcão ou no papel, e a ideia é ter um sistema onde o aluno consiga pesquisar e reservar livros pela internet, o bibliotecário controle os empréstimos e devoluções, e a coordenação acompanhe como está o uso da biblioteca.

O sistema também precisa conversar com o sistema acadêmico da universidade, para saber quem é aluno ativo e para avisar quando um aluno está devendo alguma coisa para a biblioteca.

Resumindo, o sistema vai cuidar de:

- Cadastro de livros e dos exemplares de cada livro
- Empréstimo, devolução e renovação
- Reserva de livros que estão emprestados
- Cálculo e cobrança de multa por atraso
- Bloqueio de quem está devendo
- Relatórios para a coordenação

---

## 2. Atores

Ator é quem usa o sistema ou conversa com ele. No nosso caso temos três pessoas e um sistema externo.

### 2.1 Aluno

É o usuário mais comum do sistema. Ele entra com a matrícula e a senha e consegue:

- Pesquisar livros no acervo
- Reservar um livro que está emprestado no momento
- Ver quais livros ele está com posse e quando tem que devolver
- Renovar um empréstimo
- Ver se tem multa em aberto

O aluno **não** consegue registrar empréstimo nem devolução — isso é feito pelo bibliotecário no balcão.

### 2.2 Bibliotecário

É o funcionário que trabalha no atendimento. Ele faz o trabalho do dia a dia:

- Cadastra, edita e remove livros e exemplares
- Registra empréstimos e devoluções
- Registra o pagamento de multas
- Consulta a situação de qualquer aluno
- Cancela reservas quando precisa

### 2.3 Coordenador

É quem gerencia a biblioteca. Ele consegue fazer tudo que o bibliotecário faz, e além disso:

- Gera relatórios (livros mais emprestados, atrasos, multas, movimentação)
- Muda as configurações do sistema, como prazo de empréstimo, valor da multa por dia e quantos livros cada aluno pode pegar
- Pode perdoar (cancelar) uma multa em casos específicos

### 2.4 Sistema Acadêmico (ator externo)

Não é uma pessoa, é outro sistema da universidade. Ele é usado para:

- Confirmar se a matrícula do aluno existe e está ativa
- Receber do sistema da biblioteca a informação de que o aluno está inadimplente, para que o acadêmico bloqueie a rematrícula ou a emissão de documentos

---

## 3. Requisitos Funcionais

Requisito funcional é o que o sistema tem que fazer.

| Código | Nome | Descrição |
|---|---|---|
| RF01 | Login | O sistema deve permitir que o usuário entre com matrícula/login e senha. Dependendo do perfil (aluno, bibliotecário ou coordenador), ele vê telas e opções diferentes. |
| RF02 | Cadastro de usuários | O bibliotecário e o coordenador devem conseguir cadastrar, editar, consultar e desativar usuários do sistema. Os dados básicos são nome, matrícula, curso, e-mail, telefone e perfil. |
| RF03 | Cadastro de livros | O bibliotecário deve conseguir cadastrar, editar, consultar e remover livros. Cada livro tem título, autor, editora, ano, ISBN, categoria e a quantidade de exemplares. |
| RF04 | Consulta ao acervo | Qualquer usuário logado deve conseguir pesquisar livros por título, autor ou categoria. O resultado mostra quantos exemplares existem e quantos estão disponíveis no momento. |
| RF05 | Empréstimo | O bibliotecário registra o empréstimo de um exemplar para um aluno. O sistema calcula sozinho a data de devolução com base no prazo configurado e marca o exemplar como emprestado. |
| RF06 | Devolução | O bibliotecário registra a devolução. O sistema libera o exemplar, e se a devolução foi depois do prazo, gera a multa automaticamente. |
| RF07 | Renovação | O aluno deve conseguir renovar um empréstimo pelo sistema, sem ir até a biblioteca. A renovação só é permitida se o livro não estiver reservado por outra pessoa e se o aluno não estiver bloqueado. |
| RF08 | Reserva | Quando todos os exemplares de um livro estão emprestados, o aluno deve conseguir entrar em uma fila de reserva. Quando um exemplar for devolvido, o primeiro da fila é avisado e o exemplar fica guardado para ele por um prazo. |
| RF09 | Controle de multa | O sistema deve calcular a multa por atraso automaticamente, mostrar o valor para o aluno e permitir que o bibliotecário registre o pagamento. |
| RF10 | Bloqueio de inadimplente | Aluno com multa em aberto ou com livro atrasado fica bloqueado e não consegue fazer novos empréstimos, renovações ou reservas até resolver a pendência. |
| RF11 | Integração com o sistema acadêmico | O sistema deve consultar o sistema acadêmico para validar se a matrícula do aluno está ativa, e informar quando um aluno está inadimplente com a biblioteca. |
| RF12 | Relatórios gerenciais | O coordenador deve conseguir gerar relatórios de livros mais emprestados, empréstimos em atraso, total de multas e movimentação por período. |
| RF13 | Histórico do aluno | O aluno deve conseguir ver a lista dos livros que já pegou emprestado, com as datas de retirada e devolução. |
| RF14 | Configuração de parâmetros | O coordenador deve conseguir alterar o prazo de empréstimo, o valor da multa por dia, o limite de livros por aluno e o número máximo de renovações. |

---

## 4. Regras de Negócio

São as regras que o sistema precisa seguir na hora de executar os requisitos acima.

| Código | Regra |
|---|---|
| RN01 | Cada aluno pode ter no máximo **3 livros** emprestados ao mesmo tempo. |
| RN02 | O prazo padrão de empréstimo é de **7 dias**. |
| RN03 | A multa é de **R$ 1,00 por dia de atraso, por livro**. |
| RN04 | Cada empréstimo pode ser renovado no máximo **2 vezes**. |
| RN05 | Não é possível renovar um livro que tenha alguém na fila de reserva. |
| RN06 | Aluno com multa em aberto ou livro atrasado fica bloqueado para novos empréstimos, renovações e reservas. |
| RN07 | Quando um exemplar reservado é devolvido, ele fica guardado por **48 horas** para o primeiro da fila. Se ele não retirar, passa para o próximo. |
| RN08 | Um livro só pode ser emprestado se tiver pelo menos um exemplar disponível. |
| RN09 | Só é possível reservar um livro quando todos os exemplares estiverem emprestados. |
| RN10 | Os valores de prazo, multa, limite e renovações são configuráveis pelo coordenador (RF14), os valores acima são apenas o padrão. |

---

## 5. Requisitos Não Funcionais

Requisito não funcional é sobre **como** o sistema funciona: velocidade, segurança, facilidade de uso, etc.

| Código | Tipo | Descrição |
|---|---|---|
| RNF01 | Desempenho | A pesquisa no acervo deve retornar o resultado em no máximo 3 segundos. |
| RNF02 | Segurança | As senhas devem ser guardadas criptografadas no banco, nunca em texto puro. |
| RNF03 | Segurança | Cada usuário só pode acessar o que o perfil dele permite. Um aluno não pode abrir telas de bibliotecário ou coordenador, nem pelo endereço direto da página. |
| RNF04 | Usabilidade | As telas devem ser simples e parecidas entre si, para que um aluno consiga usar o sistema sem treinamento. |
| RNF05 | Disponibilidade | O sistema deve ficar no ar durante todo o horário de funcionamento da biblioteca. |
| RNF06 | Confiabilidade | O sistema deve fazer backup do banco de dados todo dia. |
| RNF07 | Compatibilidade | O sistema deve funcionar nos navegadores mais usados (Chrome, Firefox e Edge) e se adaptar à tela do celular. |
| RNF08 | Manutenibilidade | O código deve ficar em um repositório no GitHub, com commits de todos os integrantes do grupo. |

---

## 6. Resumo

| Item | Quantidade |
|---|---|
| Atores | 4 (3 usuários + 1 sistema externo) |
| Requisitos funcionais | 14 |
| Regras de negócio | 10 |
| Requisitos não funcionais | 8 |

O mínimo pedido pela atividade era 8 requisitos funcionais e 4 não funcionais, então os dois foram atendidos.
