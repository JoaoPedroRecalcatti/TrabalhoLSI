# -*- coding: utf-8 -*-
"""
Gera os 4 diagramas UML da Etapa 2 em formato .drawio (Draw.io / diagrams.net).

Grupo: Joao Pedro Recalcatti e Sidney Alves Junior
Caso 1 - Sistema de Gestao de Biblioteca Universitaria

Uso:  python gerar_diagramas.py
"""
import html

# ---------------------------------------------------------------- infra XML

def esc(s):
    return html.escape(s, quote=True)

class Doc:
    """Acumula celulas mxGraph e escreve o arquivo .drawio."""

    def __init__(self, nome):
        self.nome = nome
        self.cells = []
        self._n = 0

    def _id(self, prefixo):
        self._n += 1
        return "%s%d" % (prefixo, self._n)

    def node(self, valor, x, y, w, h, style, parent="1", cid=None):
        cid = cid or self._id("n")
        self.cells.append(
            '<mxCell id="%s" value="%s" style="%s" vertex="1" parent="%s">'
            '<mxGeometry x="%s" y="%s" width="%s" height="%s" as="geometry"/>'
            "</mxCell>" % (cid, esc(valor), style, parent, x, y, w, h)
        )
        return cid

    def child(self, valor, y, w, h, style, parent):
        cid = self._id("c")
        self.cells.append(
            '<mxCell id="%s" value="%s" style="%s" vertex="1" parent="%s">'
            '<mxGeometry y="%s" width="%s" height="%s" as="geometry"/>'
            "</mxCell>" % (cid, esc(valor), style, parent, y, w, h)
        )
        return cid

    def edge(self, origem, destino, style, valor="", pontos=None,
             src_label=None, tgt_label=None):
        cid = self._id("e")
        geo = '<mxGeometry relative="1" as="geometry">'
        if pontos:
            geo += '<Array as="points">'
            for (px, py) in pontos:
                geo += '<mxPoint x="%s" y="%s"/>' % (px, py)
            geo += "</Array>"
        geo += "</mxGeometry>"
        self.cells.append(
            '<mxCell id="%s" value="%s" style="%s" edge="1" parent="1" '
            'source="%s" target="%s">%s</mxCell>'
            % (cid, esc(valor), style, origem, destino, geo)
        )
        if src_label:
            self._rotulo(cid, src_label, -0.75)
        if tgt_label:
            self._rotulo(cid, tgt_label, 0.75)
        return cid

    def linha(self, style, valor, x1, y1, x2, y2):
        """Aresta solta, presa a coordenadas absolutas (usada na sequencia)."""
        cid = self._id("l")
        self.cells.append(
            '<mxCell id="%s" value="%s" style="%s" edge="1" parent="1">'
            '<mxGeometry relative="1" as="geometry">'
            '<mxPoint x="%s" y="%s" as="sourcePoint"/>'
            '<mxPoint x="%s" y="%s" as="targetPoint"/>'
            "</mxGeometry></mxCell>"
            % (cid, esc(valor), style, x1, y1, x2, y2)
        )
        return cid

    def _rotulo(self, pai, texto, pos):
        cid = self._id("r")
        self.cells.append(
            '<mxCell id="%s" value="%s" style="edgeLabel;html=1;align=center;'
            'verticalAlign=middle;resizable=0;points=[];fontSize=11;" '
            'vertex="1" connectable="0" parent="%s">'
            '<mxGeometry x="%s" relative="1" as="geometry">'
            '<mxPoint as="offset"/></mxGeometry></mxCell>'
            % (cid, esc(texto), pai, pos)
        )

    def salvar(self, caminho):
        corpo = "".join(self.cells)
        xml = (
            '<mxfile host="app.diagrams.net" type="device">'
            '<diagram name="%s" id="%s">'
            '<mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" '
            'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
            'pageWidth="1169" pageHeight="826" math="0" shadow="0">'
            "<root>"
            '<mxCell id="0"/><mxCell id="1" parent="0"/>'
            "%s"
            "</root></mxGraphModel></diagram></mxfile>"
            % (esc(self.nome), self.nome.replace(" ", "-").lower(), corpo)
        )
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(xml)
        print("gerado:", caminho)


# ---------------------------------------------------- estilos reutilizaveis

ATOR = ("shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;"
        "html=1;outlineConnect=0;fontSize=12;")
UC = ("ellipse;whiteSpace=wrap;html=1;fontSize=12;fillColor=#ffffff;"
      "strokeColor=#000000;")
FRONTEIRA = ("rounded=0;whiteSpace=wrap;html=1;verticalAlign=top;fillColor=none;"
             "strokeColor=#000000;fontSize=13;fontStyle=1;")
ASSOC = "endArrow=none;html=1;rounded=0;strokeColor=#000000;"
DEP = ("endArrow=open;endSize=12;dashed=1;html=1;rounded=0;fontSize=11;"
       "strokeColor=#000000;verticalAlign=bottom;")
HERANCA = "endArrow=block;endFill=0;html=1;rounded=0;strokeColor=#000000;"


# ------------------------------------------------ 1) DIAGRAMA DE CASOS DE USO

def casos_de_uso():
    d = Doc("Casos de Uso")

    d.node("Sistema de Gestão de Biblioteca Universitária",
           135, 40, 895, 760, FRONTEIRA)

    aluno = d.node("Aluno", 70, 300, 30, 60, ATOR)
    sisacad = d.node("Sistema Acadêmico", 60, 620, 30, 60, ATOR)
    biblio = d.node("Bibliotecário", 1070, 340, 30, 60, ATOR)
    coord = d.node("Coordenador", 1070, 660, 30, 60, ATOR)

    uc_login = d.node("Fazer Login", 482.5, 90, 200, 60, UC)
    uc_valida = d.node("Validar Situação do Leitor", 485, 260, 200, 60, UC)
    uc_multa = d.node("Gerar Multa", 482.5, 400, 200, 60, UC)

    uc_acervo = d.node("Consultar Acervo", 220, 170, 200, 60, UC)
    uc_reserva = d.node("Reservar Livro", 220, 270, 200, 60, UC)
    uc_renova = d.node("Renovar Empréstimo", 220, 365, 200, 60, UC)
    uc_hist = d.node("Consultar Histórico", 220, 460, 200, 60, UC)

    uc_notif = d.node("Notificar Inadimplência", 220, 560, 200, 60, UC)
    uc_matr = d.node("Validar Matrícula Ativa", 220, 670, 200, 60, UC)

    uc_emp = d.node("Registrar Empréstimo", 770, 160, 200, 60, UC)
    uc_dev = d.node("Registrar Devolução", 770, 250, 200, 60, UC)
    uc_pag = d.node("Registrar Pagamento de Multa", 770, 350, 200, 60, UC)
    uc_cadlivro = d.node("Cadastrar Livro", 770, 440, 200, 60, UC)
    uc_cadusu = d.node("Cadastrar Usuário", 770, 540, 200, 60, UC)
    uc_rel = d.node("Gerar Relatórios", 600, 610, 200, 60, UC)
    uc_param = d.node("Configurar Parâmetros", 600, 700, 200, 60, UC)

    esq = "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"
    dir_ = "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;"

    for uc in (uc_acervo, uc_reserva, uc_renova, uc_hist):
        d.edge(aluno, uc, ASSOC + esq)
    d.edge(aluno, uc_login, ASSOC +
           "exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;",
           pontos=[(85, 100)])

    for uc in (uc_notif, uc_matr):
        d.edge(sisacad, uc, ASSOC + esq)

    for uc in (uc_emp, uc_dev, uc_pag, uc_cadlivro, uc_cadusu):
        d.edge(biblio, uc, ASSOC + dir_)
    d.edge(biblio, uc_login, ASSOC +
           "exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;",
           pontos=[(1085, 100)])

    for uc in (uc_rel, uc_param):
        d.edge(coord, uc, ASSOC + dir_)

    # o coordenador faz tudo que o bibliotecário faz (generalização de ator)
    d.edge(coord, biblio, HERANCA +
           "exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;")

    # <<include>>: a mesma validação é reaproveitada em dois casos de uso
    d.edge(uc_emp, uc_valida, DEP, "&laquo;include&raquo;")
    d.edge(uc_renova, uc_valida, DEP, "&laquo;include&raquo;")

    # <<extend>>: só acontece se a devolução estiver atrasada (RN03)
    d.edge(uc_multa, uc_dev, DEP, "&laquo;extend&raquo;")

    d.salvar("01-casos-de-uso.drawio")


# --------------------------------------------------- 2) DIAGRAMA DE CLASSES
# Os nomes de classes, atributos e métodos ficam sem acento de propósito:
# eles viram identificadores de código na Etapa 3.

LARG_CLASSE = 300
ALT_LINHA = 24

CLASSE = ("swimlane;fontStyle=1;align=center;verticalAlign=top;"
          "childLayout=stackLayout;horizontal=1;startSize=28;horizontalStack=0;"
          "resizeParent=1;resizeParentMax=0;html=1;strokeColor=#000000;"
          "fillColor=#ffffff;collapsible=0;marginBottom=0;fontSize=13;")
LINHA_ATTR = ("text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;"
              "spacingLeft=6;spacingRight=6;overflow=hidden;rotatable=0;"
              "points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontSize=11;")
SEPARADOR = ("line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;"
             "spacingTop=-1;spacingLeft=3;spacingRight=3;rotatable=0;"
             "labelPosition=right;points=[];portConstraint=eastwest;")

ORTO = "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#000000;fontSize=11;"
GENER = ORTO + "endArrow=block;endFill=0;endSize=12;"
COMPOSICAO = ORTO + "endArrow=none;startArrow=diamondThin;startFill=1;startSize=14;"
AGREGACAO = ORTO + "endArrow=none;startArrow=diamondThin;startFill=0;startSize=14;"
ASSOC_C = ORTO + "endArrow=none;"


def ponto(ex, ey, nx, ny):
    return ("exitX=%s;exitY=%s;exitDx=0;exitDy=0;"
            "entryX=%s;entryY=%s;entryDx=0;entryDy=0;" % (ex, ey, nx, ny))


def classe(d, nome, x, y, atributos, metodos, abstrata=False):
    style = CLASSE + ("fontStyle=3;" if abstrata else "")
    altura = 28 + (len(atributos) + len(metodos)) * ALT_LINHA + 8
    cid = d.node(nome, x, y, LARG_CLASSE, altura, style)
    pos = 28
    for a in atributos:
        d.child(a, pos, LARG_CLASSE, ALT_LINHA, LINHA_ATTR, cid)
        pos += ALT_LINHA
    d.child("", pos, LARG_CLASSE, 8, SEPARADOR, cid)
    pos += 8
    for m in metodos:
        d.child(m, pos, LARG_CLASSE, ALT_LINHA, LINHA_ATTR, cid)
        pos += ALT_LINHA
    return cid


def classes():
    d = Doc("Diagrama de Classes")

    autor = classe(d, "Autor", 40, 40,
        ["- id: int", "- nome: String", "- paisNascimento: String"], [])

    categoria = classe(d, "Categoria", 40, 230,
        ["- id: int", "- nome: String", "- descricao: String"], [])

    livro = classe(d, "Livro", 440, 40,
        ["- id: int", "- titulo: String", "- isbn: String",
         "- editora: String", "- anoPublicacao: int", "- edicao: String"],
        ["+ qtdExemplaresDisponiveis(): int",
         "+ possuiExemplarDisponivel(): boolean"])

    exemplar = classe(d, "Exemplar", 440, 400,
        ["- codigo: String", "- estadoConservacao: String", "- status: String"],
        ["+ estaDisponivel(): boolean",
         "+ marcarComoEmprestado(): void",
         "+ marcarComoDisponivel(): void"])

    reserva = classe(d, "Reserva", 440, 720,
        ["- id: int", "- dataHora: Date", "- status: String",
         "- dataLimiteRetirada: Date"],
        ["+ cancelar(): void", "+ expirou(): boolean", "+ posicaoNaFila(): int"])

    usuario = classe(d, "Usuario", 860, 40,
        ["# id: int", "# nome: String", "# email: String",
         "# senha: String", "# ativo: boolean"],
        ["+ autenticar(senha: String): boolean",
         "+ alterarSenha(nova: String): void",
         "+ getPerfil(): String"],
        abstrata=True)

    aluno = classe(d, "Aluno", 860, 380,
        ["- matricula: String", "- curso: String", "- bloqueado: boolean"],
        ["+ estaBloqueado(): boolean",
         "+ possuiMultaEmAberto(): boolean",
         "+ qtdEmprestimosAtivos(): int",
         "+ podePegarEmprestado(): boolean"])

    bibliotecario = classe(d, "Bibliotecario", 1300, 380,
        ["- siape: String"],
        ["+ registrarEmprestimo(a, e): Emprestimo",
         "+ registrarDevolucao(emp): void",
         "+ registrarPagamento(m: Multa): void"])

    coordenador = classe(d, "Coordenador", 1300, 640,
        ["- nivelAcesso: int"],
        ["+ gerarRelatorio(tipo, ini, fim)",
         "+ configurarParametros(p): void",
         "+ cancelarMulta(m: Multa): void"])

    emprestimo = classe(d, "Emprestimo", 880, 720,
        ["- id: int", "- dataRetirada: Date", "- dataPrevista: Date",
         "- dataDevolucao: Date", "- qtdRenovacoes: int"],
        ["+ estaAtrasado(): boolean",
         "+ diasDeAtraso(): int",
         "+ podeRenovar(): boolean",
         "+ renovar(): boolean",
         "+ calcularMulta(): double"])

    multa = classe(d, "Multa", 880, 1080,
        ["- id: int", "- valor: double", "- status: String",
         "- dataPagamento: Date"],
        ["+ pagar(): void", "+ estaEmAberto(): boolean"])

    parametros = classe(d, "ParametrosSistema", 1310, 1070,
        ["- prazoEmprestimoDias: int", "- valorMultaPorDia: double",
         "- limiteLivrosPorAluno: int", "- maxRenovacoes: int"],
        ["+ getInstancia(): ParametrosSistema"])

    # ---- herança (exigida pelo enunciado)
    d.edge(aluno, usuario, GENER + ponto(0.5, 0, 0.5, 1))
    d.edge(bibliotecario, usuario, GENER + ponto(0.5, 0, 1, 0.5))
    d.edge(coordenador, bibliotecario, GENER + ponto(0.5, 0, 0.5, 1))

    # ---- composição: o exemplar não existe sem o livro
    d.edge(livro, exemplar, COMPOSICAO + ponto(0.5, 1, 0.5, 0),
           "possui", src_label="1", tgt_label="1..*")

    # ---- agregação: o autor existe independentemente do livro
    d.edge(livro, autor, AGREGACAO + ponto(0, 0.3, 1, 0.5),
           "escrito por", src_label="1..*", tgt_label="1..*")

    # ---- associações (com corredores livres para não cruzar as caixas)
    d.edge(livro, categoria, ASSOC_C + ponto(0, 0.8, 1, 0.3),
           "classificado em", src_label="0..*", tgt_label="1..*")
    d.edge(livro, reserva, ASSOC_C + ponto(0, 0.95, 0, 0.3),
           "fila de espera de", src_label="1", tgt_label="0..*",
           pontos=[(390, 257), (390, 781)])
    d.edge(exemplar, emprestimo, ASSOC_C + ponto(1, 0.5, 0, 0.3),
           "refere-se a", src_label="1", tgt_label="0..*",
           pontos=[(810, 490), (810, 803)])
    d.edge(aluno, reserva, ASSOC_C + ponto(0, 0.8, 1, 0.3),
           "faz", src_label="1", tgt_label="0..*",
           pontos=[(800, 543), (800, 781)])
    d.edge(aluno, emprestimo, ASSOC_C + ponto(0.5, 1, 0.5, 0),
           "realiza", src_label="1", tgt_label="0..*")
    d.edge(bibliotecario, emprestimo, ASSOC_C + ponto(0, 0.5, 1, 0.3),
           "registra", src_label="1", tgt_label="0..*",
           pontos=[(1240, 446), (1240, 803)])
    d.edge(emprestimo, multa, ASSOC_C + ponto(0.5, 1, 0.5, 0),
           "gera", src_label="1", tgt_label="0..1")
    d.edge(emprestimo, parametros, ASSOC_C + ponto(1, 0.8, 0, 0.5),
           "usa", src_label="0..*", tgt_label="1",
           pontos=[(1245, 941), (1245, 1158)])

    d.salvar("02-classes.drawio")


# ------------------------------------------------- 3) DIAGRAMA DE SEQUENCIA

LIFELINE = ("shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;html=1;"
            "container=0;collapsible=0;recursiveResize=0;outlineConnect=0;size=50;"
            "strokeColor=#000000;fillColor=#ffffff;fontSize=12;")
LIFELINE_ATOR = (LIFELINE + "participant=umlActor;verticalAlign=top;"
                 "spacingTop=64;size=64;")
MSG = ("html=1;verticalAlign=bottom;endArrow=block;endFill=1;rounded=0;"
       "strokeColor=#000000;fontSize=11;align=center;")
RETORNO = ("html=1;verticalAlign=bottom;endArrow=open;endSize=10;dashed=1;rounded=0;"
           "strokeColor=#000000;fontSize=11;align=center;")
FRAME = ("shape=umlFrame;whiteSpace=wrap;html=1;width=70;height=28;fontSize=12;"
         "strokeColor=#000000;fillColor=none;align=left;verticalAlign=top;")
ATIVACAO = ("html=1;points=[];perimeter=orthogonalPerimeter;fillColor=#ffffff;"
            "strokeColor=#000000;")
DIVISOR = "endArrow=none;dashed=1;html=1;rounded=0;strokeColor=#000000;"
COND = "text;html=1;align=left;fontSize=11;fontStyle=1;"


def sequencia():
    d = Doc("Sequência - Registrar Devolução")

    largura, passo, topo, altura = 170, 210, 40, 1030
    nomes = ["Bibliotecário", ":TelaDevolucao", ":ControladorEmprestimo",
             ":Emprestimo", ":ParametrosSistema", ":Multa", ":Aluno",
             ":Exemplar", ":FilaReserva"]
    cx = {}
    for i, nome in enumerate(nomes):
        x = 40 + i * passo
        centro = x + largura / 2.0
        if i == 0:
            d.node(nome, centro - 20, topo, 40, altura, LIFELINE_ATOR)
        else:
            d.node(nome, x, topo, largura, altura, LIFELINE)
        cx[nome] = centro

    B, T, C = cx["Bibliotecário"], cx[":TelaDevolucao"], cx[":ControladorEmprestimo"]
    E, P, M = cx[":Emprestimo"], cx[":ParametrosSistema"], cx[":Multa"]
    A, X, F = cx[":Aluno"], cx[":Exemplar"], cx[":FilaReserva"]

    d.node("", C - 8, 205, 16, 790, ATIVACAO)

    def msg(txt, x1, x2, y, estilo=MSG):
        d.linha(estilo, txt, x1, y, x2, y)

    msg("1: informarCodigoExemplar(codigo)", B, T, 160)
    msg("2: registrarDevolucao(codigo)", T, C, 205)
    msg("3: buscarEmprestimoAtivo(codigo)", C, E, 250)
    msg("4: emprestimo", E, C, 288, RETORNO)
    msg("5: estaAtrasado()", C, E, 330)
    msg("6: true", E, C, 368, RETORNO)

    # alt: devolução em atraso x devolução em dia (RN03)
    d.node("alt", 470, 395, 1010, 300, FRAME)
    d.node("[devolução em atraso]", 490, 425, 220, 20, COND)
    msg("7: getValorMultaPorDia()", C, P, 465)
    msg("8: valorPorDia", P, C, 503, RETORNO)
    msg("9: calcularMulta(valorPorDia, diasDeAtraso)", C, E, 540)
    msg("10: valorMulta", E, C, 578, RETORNO)
    msg("11: criar(emprestimo, valorMulta)", C, M, 615)
    msg("12: bloquear()", C, A, 652)
    d.linha(DIVISOR, "", 470, 675, 1480, 675)
    d.node("[devolução em dia]", 490, 678, 220, 18, COND)

    msg("13: marcarComoDisponivel()", C, X, 735)
    msg("14: existeReservaPara(livro)", C, F, 778)
    msg("15: true", F, C, 816, RETORNO)

    # opt: só notifica se houver alguém na fila (RN07)
    d.node("opt", 470, 840, 1380, 90, FRAME)
    d.node("[existe reserva para o livro]", 490, 870, 250, 20, COND)
    msg("16: notificarPrimeiroDaFila()", C, F, 908)

    msg("17: devolucaoRegistrada(valorMulta)", C, T, 955, RETORNO)
    msg("18: exibirResultado()", T, B, 992, RETORNO)

    d.node("Caso de uso crítico: Registrar Devolução.&#10;"
           "Cobre RF06 (devolução), RF09 (multa), RF10 (bloqueio) e "
           "RF08 (fila de reserva).&#10;"
           "Regras aplicadas: RN03 (R$ 1,00 por dia de atraso), "
           "RN06 (bloqueio do inadimplente) e RN07 (48h para o primeiro da fila).",
           40, 1100, 940, 80,
           "shape=note;whiteSpace=wrap;html=1;size=14;fontSize=11;align=left;"
           "verticalAlign=top;spacingLeft=6;")

    d.salvar("03-sequencia-registrar-devolucao.drawio")


# ------------------------------------------------- 4) DIAGRAMA DE ATIVIDADES

INICIO = "ellipse;html=1;fillColor=#000000;strokeColor=#000000;"
FIM = "ellipse;html=1;shape=endState;fillColor=#000000;strokeColor=#000000;"
ACAO = ("rounded=1;arcSize=40;whiteSpace=wrap;html=1;fillColor=#ffffff;"
        "strokeColor=#000000;fontSize=12;")
DECISAO = ("rhombus;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;"
           "fontSize=12;")
BARRA = "rounded=0;html=1;fillColor=#000000;strokeColor=#000000;"
FLUXO = ("edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=1;"
         "strokeColor=#000000;fontSize=11;")


def atividades():
    d = Doc("Atividades - Realizar Empréstimo")

    ini = d.node("", 380, 40, 40, 40, INICIO)
    a1 = d.node("Bibliotecário identifica o aluno e o exemplar",
                250, 130, 300, 50, ACAO)
    fork = d.node("", 200, 240, 400, 10, BARRA)
    a2 = d.node("Verificar a situação do aluno (bloqueio, multa em aberto "
                "e limite de livros)", 60, 300, 260, 80, ACAO)
    a3 = d.node("Verificar a disponibilidade do exemplar",
                480, 300, 260, 80, ACAO)
    join = d.node("", 200, 430, 400, 10, BARRA)
    dec = d.node("Aluno liberado e exemplar disponível?",
                 300, 480, 200, 110, DECISAO)
    rec = d.node("Exibir o motivo da recusa ao bibliotecário",
                 640, 500, 220, 70, ACAO)
    fim2 = d.node("", 730, 640, 40, 40, FIM)
    a4 = d.node("Calcular a data prevista de devolução (prazo padrão: 7 dias)",
                250, 640, 300, 60, ACAO)
    a5 = d.node("Registrar o empréstimo e marcar o exemplar como Emprestado",
                250, 750, 300, 60, ACAO)
    a6 = d.node("Entregar o exemplar ao aluno", 250, 860, 300, 50, ACAO)
    fim = d.node("", 380, 960, 40, 40, FIM)

    d.edge(ini, a1, FLUXO)
    d.edge(a1, fork, FLUXO)
    d.edge(fork, a2, FLUXO)   # paralelismo: as duas verificações são independentes
    d.edge(fork, a3, FLUXO)
    d.edge(a2, join, FLUXO)
    d.edge(a3, join, FLUXO)
    d.edge(join, dec, FLUXO)
    d.edge(dec, rec, FLUXO, "[não]")
    d.edge(rec, fim2, FLUXO)
    d.edge(dec, a4, FLUXO, "[sim]")
    d.edge(a4, a5, FLUXO)
    d.edge(a5, a6, FLUXO)
    d.edge(a6, fim, FLUXO)

    d.node("Paralelismo (fork/join): verificar a situação do aluno e verificar "
           "a disponibilidade do exemplar são atividades independentes e "
           "acontecem ao mesmo tempo.&#10;"
           "Decisão: o empréstimo só é liberado se as duas passarem "
           "(RN01, RN06 e RN08).",
           640, 780, 320, 120,
           "shape=note;whiteSpace=wrap;html=1;size=14;fontSize=11;align=left;"
           "verticalAlign=top;spacingLeft=6;")

    d.salvar("04-atividades-realizar-emprestimo.drawio")


if __name__ == "__main__":
    casos_de_uso()
    classes()
    sequencia()
    atividades()
