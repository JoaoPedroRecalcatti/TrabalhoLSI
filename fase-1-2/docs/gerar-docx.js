const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  PageBreak, Footer, PageNumber, LevelFormat, convertInchesToTwip,
} = require("docx");

const AZUL = "1F4E79";
const CINZA = "D9E2F3";
const W = 9000;

// ---------- helpers ----------
const cell = (text, width, opts = {}) =>
  new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: opts.header
      ? { type: ShadingType.CLEAR, fill: CINZA, color: "auto" }
      : undefined,
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [
      new Paragraph({
        alignment: opts.center ? AlignmentType.CENTER : AlignmentType.LEFT,
        spacing: { before: 0, after: 0 },
        children: [
          new TextRun({
            text,
            bold: !!opts.header || !!opts.bold,
            size: 20,
            color: opts.header ? AZUL : "000000",
          }),
        ],
      }),
    ],
  });

const tabela = (widths, header, rows) =>
  new Table({
    columnWidths: widths,
    width: { size: W, type: WidthType.DXA },
    rows: [
      new TableRow({
        tableHeader: true,
        children: header.map((h, i) =>
          cell(h, widths[i], { header: true, center: i === 0 || widths.length === 2 && i === 1 && h === "Quantidade" })
        ),
      }),
      ...rows.map(
        (r) =>
          new TableRow({
            children: r.map((c, i) =>
              cell(c, widths[i], { center: i === 0 && /^(RF|RN|RNF)\d+$/.test(c) })
            ),
          })
      ),
    ],
  });

const h1 = (t) =>
  new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 160 },
    children: [new TextRun({ text: t, bold: true, size: 30, color: AZUL })],
  });

const h2 = (t) =>
  new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 240, after: 120 },
    children: [new TextRun({ text: t, bold: true, size: 25, color: AZUL })],
  });

const p = (t, opts = {}) =>
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { after: 120, line: 300 },
    children: [new TextRun({ text: t, size: 22, bold: !!opts.bold, italics: !!opts.italics })],
  });

const li = (t) =>
  new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { after: 60, line: 300 },
    children: [new TextRun({ text: t, size: 22 })],
  });

const capaLinha = (t, opts = {}) =>
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: opts.after ?? 60 },
    children: [
      new TextRun({ text: t, size: opts.size ?? 24, bold: !!opts.bold, color: opts.color ?? "000000" }),
    ],
  });

const vazio = (n = 1) =>
  Array.from({ length: n }, () => new Paragraph({ children: [new TextRun("")] }));

// ---------- capa ----------
const capa = [
  ...vazio(1),
  capaLinha("UNIVERSIDADE ESTADUAL DE MATO GROSSO DO SUL", { bold: true, size: 26 }),
  capaLinha("CURSO DE SISTEMAS DE INFORMAÇÃO", { bold: true, size: 24, after: 240 }),
  ...vazio(4),
  capaLinha("JOÃO PEDRO RECALCATTI", { size: 24 }),
  capaLinha("SIDNEY ALVES JUNIOR", { size: 24 }),
  ...vazio(4),
  capaLinha("DOCUMENTO DE REQUISITOS", { bold: true, size: 40, color: AZUL, after: 120 }),
  capaLinha("Sistema de Gestão de Biblioteca Universitária", { size: 28, after: 0 }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 200, after: 0 },
    border: {
      bottom: { style: BorderStyle.SINGLE, size: 12, color: AZUL, space: 1 },
    },
    children: [new TextRun({ text: "", size: 22 })],
  }),
  ...vazio(4),
  new Paragraph({
    alignment: AlignmentType.RIGHT,
    indent: { left: convertInchesToTwip(2.6) },
    spacing: { after: 120, line: 300 },
    children: [
      new TextRun({
        text:
          "Atividade Prática — Modelagem e Implementação, " +
          "apresentada à disciplina de Laboratório de Sistemas de Informação " +
          "do curso de Sistemas de Informação da UEMS.",
        size: 22,
      }),
    ],
  }),
  new Paragraph({
    alignment: AlignmentType.RIGHT,
    indent: { left: convertInchesToTwip(2.6) },
    spacing: { after: 120, line: 300 },
    children: [new TextRun({ text: "Professor: France Ricardo", size: 22 })],
  }),
  new Paragraph({
    alignment: AlignmentType.RIGHT,
    indent: { left: convertInchesToTwip(2.6) },
    spacing: { after: 120, line: 300 },
    children: [new TextRun({ text: "Etapa 1 — Levantamento de Requisitos", size: 22 })],
  }),
  new Paragraph({
    alignment: AlignmentType.RIGHT,
    indent: { left: convertInchesToTwip(2.6) },
    spacing: { after: 120, line: 300 },
    children: [new TextRun({ text: "Caso 1 — Sistema de Gestão de Biblioteca Universitária", size: 22 })],
  }),
  ...vazio(5),
  capaLinha("Dourados — MS", { size: 24 }),
  capaLinha("2026", { size: 24 }),
  new Paragraph({ children: [new PageBreak()] }),
];

// ---------- conteúdo ----------
const conteudo = [
  h1("1. Sobre o sistema"),
  p(
    "A UEMS quer modernizar a biblioteca dela. Hoje muita coisa é feita no balcão ou no papel, e a ideia é ter um sistema onde o aluno consiga pesquisar e reservar livros pela internet, o bibliotecário controle os empréstimos e devoluções, e a coordenação acompanhe como está o uso da biblioteca."
  ),
  p(
    "O sistema também precisa conversar com o sistema acadêmico da universidade, para saber quem é aluno ativo e para avisar quando um aluno está devendo alguma coisa para a biblioteca."
  ),
  p("Resumindo, o sistema vai cuidar de:"),
  li("Cadastro de livros e dos exemplares de cada livro"),
  li("Empréstimo, devolução e renovação"),
  li("Reserva de livros que estão emprestados"),
  li("Cálculo e cobrança de multa por atraso"),
  li("Bloqueio de quem está devendo"),
  li("Relatórios para a coordenação"),

  h1("2. Atores"),
  p(
    "Ator é quem usa o sistema ou conversa com ele. No nosso caso temos três pessoas e um sistema externo."
  ),

  h2("2.1 Aluno"),
  p(
    "É o usuário mais comum do sistema. Ele entra com a matrícula e a senha e consegue:"
  ),
  li("Pesquisar livros no acervo"),
  li("Reservar um livro que está emprestado no momento"),
  li("Ver quais livros ele está com posse e quando tem que devolver"),
  li("Renovar um empréstimo"),
  li("Ver se tem multa em aberto"),
  p(
    "O aluno não consegue registrar empréstimo nem devolução — isso é feito pelo bibliotecário no balcão."
  ),

  h2("2.2 Bibliotecário"),
  p("É o funcionário que trabalha no atendimento. Ele faz o trabalho do dia a dia:"),
  li("Cadastra, edita e remove livros e exemplares"),
  li("Registra empréstimos e devoluções"),
  li("Registra o pagamento de multas"),
  li("Consulta a situação de qualquer aluno"),
  li("Cancela reservas quando precisa"),

  h2("2.3 Coordenador"),
  p(
    "É quem gerencia a biblioteca. Ele consegue fazer tudo que o bibliotecário faz, e além disso:"
  ),
  li("Gera relatórios (livros mais emprestados, atrasos, multas, movimentação)"),
  li(
    "Muda as configurações do sistema, como prazo de empréstimo, valor da multa por dia e quantos livros cada aluno pode pegar"
  ),
  li("Pode perdoar (cancelar) uma multa em casos específicos"),

  h2("2.4 Sistema Acadêmico (ator externo)"),
  p("Não é uma pessoa, é outro sistema da universidade. Ele é usado para:"),
  li("Confirmar se a matrícula do aluno existe e está ativa"),
  li(
    "Receber do sistema da biblioteca a informação de que o aluno está inadimplente, para que o acadêmico bloqueie a rematrícula ou a emissão de documentos"
  ),

  new Paragraph({ children: [new PageBreak()] }),

  h1("3. Requisitos Funcionais"),
  p("Requisito funcional é o que o sistema tem que fazer."),
  tabela(
    [1000, 2200, 5800],
    ["Código", "Nome", "Descrição"],
    [
      ["RF01", "Login", "O sistema deve permitir que o usuário entre com matrícula/login e senha. Dependendo do perfil (aluno, bibliotecário ou coordenador), ele vê telas e opções diferentes."],
      ["RF02", "Cadastro de usuários", "O bibliotecário e o coordenador devem conseguir cadastrar, editar, consultar e desativar usuários do sistema. Os dados básicos são nome, matrícula, curso, e-mail, telefone e perfil."],
      ["RF03", "Cadastro de livros", "O bibliotecário deve conseguir cadastrar, editar, consultar e remover livros. Cada livro tem título, autor, editora, ano, ISBN, categoria e a quantidade de exemplares."],
      ["RF04", "Consulta ao acervo", "Qualquer usuário logado deve conseguir pesquisar livros por título, autor ou categoria. O resultado mostra quantos exemplares existem e quantos estão disponíveis no momento."],
      ["RF05", "Empréstimo", "O bibliotecário registra o empréstimo de um exemplar para um aluno. O sistema calcula sozinho a data de devolução com base no prazo configurado e marca o exemplar como emprestado."],
      ["RF06", "Devolução", "O bibliotecário registra a devolução. O sistema libera o exemplar, e se a devolução foi depois do prazo, gera a multa automaticamente."],
      ["RF07", "Renovação", "O aluno deve conseguir renovar um empréstimo pelo sistema, sem ir até a biblioteca. A renovação só é permitida se o livro não estiver reservado por outra pessoa e se o aluno não estiver bloqueado."],
      ["RF08", "Reserva", "Quando todos os exemplares de um livro estão emprestados, o aluno deve conseguir entrar em uma fila de reserva. Quando um exemplar for devolvido, o primeiro da fila é avisado e o exemplar fica guardado para ele por um prazo."],
      ["RF09", "Controle de multa", "O sistema deve calcular a multa por atraso automaticamente, mostrar o valor para o aluno e permitir que o bibliotecário registre o pagamento."],
      ["RF10", "Bloqueio de inadimplente", "Aluno com multa em aberto ou com livro atrasado fica bloqueado e não consegue fazer novos empréstimos, renovações ou reservas até resolver a pendência."],
      ["RF11", "Integração com o sistema acadêmico", "O sistema deve consultar o sistema acadêmico para validar se a matrícula do aluno está ativa, e informar quando um aluno está inadimplente com a biblioteca."],
      ["RF12", "Relatórios gerenciais", "O coordenador deve conseguir gerar relatórios de livros mais emprestados, empréstimos em atraso, total de multas e movimentação por período."],
      ["RF13", "Histórico do aluno", "O aluno deve conseguir ver a lista dos livros que já pegou emprestado, com as datas de retirada e devolução."],
      ["RF14", "Configuração de parâmetros", "O coordenador deve conseguir alterar o prazo de empréstimo, o valor da multa por dia, o limite de livros por aluno e o número máximo de renovações."],
    ]
  ),

  h1("4. Regras de Negócio"),
  p("São as regras que o sistema precisa seguir na hora de executar os requisitos acima."),
  tabela(
    [1000, 8000],
    ["Código", "Regra"],
    [
      ["RN01", "Cada aluno pode ter no máximo 3 livros emprestados ao mesmo tempo."],
      ["RN02", "O prazo padrão de empréstimo é de 7 dias."],
      ["RN03", "A multa é de R$ 1,00 por dia de atraso, por livro."],
      ["RN04", "Cada empréstimo pode ser renovado no máximo 2 vezes."],
      ["RN05", "Não é possível renovar um livro que tenha alguém na fila de reserva."],
      ["RN06", "Aluno com multa em aberto ou livro atrasado fica bloqueado para novos empréstimos, renovações e reservas."],
      ["RN07", "Quando um exemplar reservado é devolvido, ele fica guardado por 48 horas para o primeiro da fila. Se ele não retirar, passa para o próximo."],
      ["RN08", "Um livro só pode ser emprestado se tiver pelo menos um exemplar disponível."],
      ["RN09", "Só é possível reservar um livro quando todos os exemplares estiverem emprestados."],
      ["RN10", "Os valores de prazo, multa, limite e renovações são configuráveis pelo coordenador (RF14), os valores acima são apenas o padrão."],
    ]
  ),

  h1("5. Requisitos Não Funcionais"),
  p(
    "Requisito não funcional é sobre como o sistema funciona: velocidade, segurança, facilidade de uso, etc."
  ),
  tabela(
    [1000, 1800, 6200],
    ["Código", "Tipo", "Descrição"],
    [
      ["RNF01", "Desempenho", "A pesquisa no acervo deve retornar o resultado em no máximo 3 segundos."],
      ["RNF02", "Segurança", "As senhas devem ser guardadas criptografadas no banco, nunca em texto puro."],
      ["RNF03", "Segurança", "Cada usuário só pode acessar o que o perfil dele permite. Um aluno não pode abrir telas de bibliotecário ou coordenador, nem pelo endereço direto da página."],
      ["RNF04", "Usabilidade", "As telas devem ser simples e parecidas entre si, para que um aluno consiga usar o sistema sem treinamento."],
      ["RNF05", "Disponibilidade", "O sistema deve ficar no ar durante todo o horário de funcionamento da biblioteca."],
      ["RNF06", "Confiabilidade", "O sistema deve fazer backup do banco de dados todo dia."],
      ["RNF07", "Compatibilidade", "O sistema deve funcionar nos navegadores mais usados (Chrome, Firefox e Edge) e se adaptar à tela do celular."],
      ["RNF08", "Manutenibilidade", "O código deve ficar em um repositório no GitHub, com commits de todos os integrantes do grupo."],
    ]
  ),

  h1("6. Resumo"),
  tabela(
    [6000, 3000],
    ["Item", "Quantidade"],
    [
      ["Atores", "4 (3 usuários + 1 sistema externo)"],
      ["Requisitos funcionais", "14"],
      ["Regras de negócio", "10"],
      ["Requisitos não funcionais", "8"],
    ]
  ),
  new Paragraph({ children: [new TextRun("")] }),
  p(
    "O mínimo pedido pela atividade era 8 requisitos funcionais e 4 não funcionais, então os dois foram atendidos."
  ),
];

// ---------- documento ----------
const doc = new Document({
  creator: "João Pedro Recalcatti e Sidney Alves Junior",
  title: "Documento de Requisitos — Sistema de Gestão de Biblioteca Universitária",
  styles: {
    default: {
      document: { run: { font: "Calibri", size: 22 } },
    },
  },
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [
          {
            level: 0,
            format: LevelFormat.BULLET,
            text: "•",
            alignment: AlignmentType.LEFT,
            style: {
              paragraph: { indent: { left: 720, hanging: 360 } },
              run: { size: 22 },
            },
          },
        ],
      },
    ],
  },
  sections: [
    {
      properties: {
        page: {
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
        },
        titlePage: true,
      },
      footers: {
        default: new Footer({
          children: [
            new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [new TextRun({ children: [PageNumber.CURRENT], size: 20 })],
            }),
          ],
        }),
        first: new Footer({ children: [new Paragraph({ children: [new TextRun("")] })] }),
      },
      children: [...capa, ...conteudo],
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(process.argv[2], buf);
  console.log("OK ->", process.argv[2]);
});
