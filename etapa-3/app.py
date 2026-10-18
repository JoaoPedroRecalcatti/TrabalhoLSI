"""
Sistema de Gestão de Biblioteca Universitária — protótipo da Etapa 3. 

Grupo: João Pedro Recalcatti e Sidney Alves Junior

Para rodar:   python app.py
Depois abra:  http://localhost:5000
"""
import os
from datetime import date
from functools import wraps

from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)

from models import (LIMITE_LIVROS, MULTA_POR_DIA, PRAZO_DIAS, Emprestimo,
                    Livro, Multa, Usuario, calcular_data_prevista, db)

app = Flask(__name__)
app.config["SECRET_KEY"] = "chave-do-trabalho-uems"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "biblioteca.db")
db.init_app(app)


# ------------------------------------------------------------------ ajudantes

def usuario_logado():
    """Devolve o usuário da sessão, ou None se ninguém está logado."""
    uid = session.get("usuario_id")
    return db.session.get(Usuario, uid) if uid else None


def precisa_login(f):
    @wraps(f)
    def dentro(*args, **kwargs):
        if usuario_logado() is None:
            flash("Faça login para entrar no sistema.", "erro")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return dentro


def precisa_bibliotecario(f):
    """RNF03 — o aluno não abre tela de bibliotecário nem digitando o endereço."""
    @wraps(f)
    def dentro(*args, **kwargs):
        u = usuario_logado()
        if u is None:
            flash("Faça login para entrar no sistema.", "erro")
            return redirect(url_for("login"))
        if not u.e_bibliotecario():
            flash("Esta tela é só para o bibliotecário.", "erro")
            return redirect(url_for("painel"))
        return f(*args, **kwargs)
    return dentro


@app.context_processor
def injetar_usuario():
    """Deixa o usuário logado disponível em todas as telas."""
    return {"usuario": usuario_logado()}


@app.template_filter("data")
def filtro_data(valor):
    return valor.strftime("%d/%m/%Y") if valor else "—"


@app.template_filter("reais")
def filtro_reais(valor):
    return f"R$ {valor:.2f}".replace(".", ",")


# ------------------------------------------------------------ 1) LOGIN (RF01)

@app.route("/")
def inicio():
    return redirect(url_for("painel") if usuario_logado() else url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        u = Usuario.query.filter_by(email=email).first()
        if u is None or not u.autenticar(senha):
            flash("E-mail ou senha inválidos.", "erro")
            return render_template("login.html", email=email)

        session["usuario_id"] = u.id
        return redirect(url_for("painel"))

    return render_template("login.html", email="")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/painel")
@precisa_login
def painel():
    u = usuario_logado()
    if u.e_bibliotecario():
        ativos = Emprestimo.query.filter_by(data_devolucao=None).all()
        return render_template(
            "painel.html",
            total_livros=Livro.query.count(),
            ativos=len(ativos),
            atrasados=[e for e in ativos if e.esta_atrasado()],
        )
    return render_template("painel.html", meus=u.emprestimos_ativos())


# --------------------------------- 2) LISTAGEM COM FILTRO — acervo (RF04)

@app.route("/acervo")
@precisa_login
def acervo():
    termo = request.args.get("termo", "").strip()
    categoria = request.args.get("categoria", "").strip()
    so_disponiveis = request.args.get("disponiveis") == "1"

    consulta = Livro.query
    if termo:
        curinga = f"%{termo}%"
        consulta = consulta.filter(
            db.or_(Livro.titulo.like(curinga), Livro.autor.like(curinga)))
    if categoria:
        consulta = consulta.filter(Livro.categoria == categoria)

    livros = consulta.order_by(Livro.titulo).all()
    if so_disponiveis:
        livros = [l for l in livros if l.tem_disponivel()]

    categorias = sorted({l.categoria for l in Livro.query.all() if l.categoria})

    return render_template("acervo.html", livros=livros, categorias=categorias,
                           termo=termo, categoria=categoria,
                           so_disponiveis=so_disponiveis)


# --------------------------------------- 3) CRUD DE LIVROS (RF03)

@app.route("/livros")
@precisa_bibliotecario
def livros():
    return render_template("livros.html",
                           livros=Livro.query.order_by(Livro.titulo).all())


@app.route("/livros/novo", methods=["GET", "POST"])
@app.route("/livros/<int:livro_id>/editar", methods=["GET", "POST"])
@precisa_bibliotecario
def livro_form(livro_id=None):
    livro = db.session.get(Livro, livro_id) if livro_id else None

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        quantidade = request.form.get("qtd_exemplares", "").strip()

        if not titulo:
            flash("O título é obrigatório.", "erro")
            return render_template("livro_form.html", livro=livro,
                                   form=request.form)
        if not quantidade.isdigit() or int(quantidade) < 1:
            flash("A quantidade de exemplares deve ser um número maior que zero.",
                  "erro")
            return render_template("livro_form.html", livro=livro,
                                   form=request.form)

        if livro is None:
            livro = Livro()
            db.session.add(livro)

        # não deixa reduzir abaixo do que já está emprestado
        if int(quantidade) < livro.qtd_emprestados():
            flash(f"Existem {livro.qtd_emprestados()} exemplares emprestados. "
                  "A quantidade não pode ser menor que isso.", "erro")
            return render_template("livro_form.html", livro=livro,
                                   form=request.form)

        livro.titulo = titulo
        livro.autor = request.form.get("autor", "").strip()
        livro.editora = request.form.get("editora", "").strip()
        livro.categoria = request.form.get("categoria", "").strip()
        ano = request.form.get("ano", "").strip()
        livro.ano = int(ano) if ano.isdigit() else None
        livro.qtd_exemplares = int(quantidade)

        db.session.commit()
        flash("Livro salvo.", "ok")
        return redirect(url_for("livros"))

    return render_template("livro_form.html", livro=livro, form=None)


@app.route("/livros/<int:livro_id>/excluir", methods=["POST"])
@precisa_bibliotecario
def livro_excluir(livro_id):
    livro = db.session.get(Livro, livro_id)
    if livro is None:
        flash("Livro não encontrado.", "erro")
    elif livro.qtd_emprestados() > 0:
        flash("Não dá para excluir: este livro tem exemplares emprestados.", "erro")
    else:
        Emprestimo.query.filter_by(livro_id=livro.id).delete()
        db.session.delete(livro)
        db.session.commit()
        flash("Livro excluído.", "ok")
    return redirect(url_for("livros"))


# ------------------- 4) REGRA DE NEGÓCIO — empréstimo e devolução com multa

@app.route("/emprestimos", methods=["GET", "POST"])
@precisa_bibliotecario
def emprestimos():
    if request.method == "POST":
        aluno = livro = None
        if request.form.get("aluno_id", "").isdigit():
            aluno = db.session.get(Usuario, int(request.form["aluno_id"]))
        if request.form.get("livro_id", "").isdigit():
            livro = db.session.get(Livro, int(request.form["livro_id"]))

        erro = None
        if aluno is None or livro is None:
            erro = "Escolha o aluno e o livro."
        elif aluno.tem_multa_em_aberto():
            erro = f"{aluno.nome} tem multa em aberto e está bloqueado (RN06)."
        elif len(aluno.emprestimos_ativos()) >= LIMITE_LIVROS:
            erro = f"{aluno.nome} já está com {LIMITE_LIVROS} livros (RN01)."
        elif not livro.tem_disponivel():
            erro = f"Não há exemplar disponível de '{livro.titulo}' (RN08)."

        if erro:
            flash(erro, "erro")
        else:
            novo = Emprestimo(aluno=aluno, livro=livro,
                              data_retirada=date.today(),
                              data_prevista=calcular_data_prevista())
            db.session.add(novo)
            db.session.commit()
            flash(f"Empréstimo registrado. Devolver até "
                  f"{novo.data_prevista.strftime('%d/%m/%Y')}.", "ok")
        return redirect(url_for("emprestimos"))

    return render_template(
        "emprestimos.html",
        ativos=Emprestimo.query.filter_by(data_devolucao=None)
                               .order_by(Emprestimo.data_prevista).all(),
        alunos=Usuario.query.filter_by(perfil="aluno")
                            .order_by(Usuario.nome).all(),
        livros=Livro.query.order_by(Livro.titulo).all(),
        multas=Multa.query.filter_by(status="Em aberto").all(),
        prazo=PRAZO_DIAS,
    )


@app.route("/emprestimos/<int:emprestimo_id>/devolver", methods=["POST"])
@precisa_bibliotecario
def devolver(emprestimo_id):
    """
    Aqui roda a regra de negócio do trabalho.

    É o mesmo caminho do diagrama de sequência: registra a devolução,
    verifica se atrasou, calcula a multa e cria a multa se for o caso.
    """
    emprestimo = db.session.get(Emprestimo, emprestimo_id)
    if emprestimo is None or emprestimo.devolvido():
        flash("Empréstimo não encontrado ou já devolvido.", "erro")
        return redirect(url_for("emprestimos"))

    emprestimo.data_devolucao = date.today()

    if emprestimo.esta_atrasado():
        dias = emprestimo.dias_de_atraso()
        valor = emprestimo.calcular_multa()
        emprestimo.multa = Multa(valor=valor)
        flash(f"Devolução registrada com {dias} dia(s) de atraso. "
              f"Multa de R$ {valor:.2f} gerada para {emprestimo.aluno.nome}."
              .replace(".", ","), "aviso")
    else:
        flash("Devolução registrada no prazo. Sem multa.", "ok")

    db.session.commit()
    return redirect(url_for("emprestimos"))


@app.route("/multas/<int:multa_id>/pagar", methods=["POST"])
@precisa_bibliotecario
def pagar_multa(multa_id):
    multa = db.session.get(Multa, multa_id)
    if multa and multa.status == "Em aberto":
        multa.pagar()
        db.session.commit()
        flash(f"Multa de {multa.emprestimo.aluno.nome} quitada.", "ok")
    return redirect(url_for("emprestimos"))


@app.route("/meus-emprestimos")
@precisa_login
def meus_emprestimos():
    u = usuario_logado()
    return render_template("meus_emprestimos.html",
                           emprestimos=u.emprestimos,
                           multa_por_dia=MULTA_POR_DIA)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
