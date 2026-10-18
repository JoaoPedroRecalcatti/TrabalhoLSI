"""
Modelos do sistema — só 4 tabelas.

Usuario, Livro, Emprestimo e Multa. 
Cada uma corresponde a uma classe do diagrama de classes da Etapa 2.
"""
from datetime import date, timedelta

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

# --------------------------------------------------------------------------
# Regras de negócio do documento de requisitos (Etapa 1).
# Ficam aqui em cima, num lugar só, para ficar fácil de achar e de mostrar.
# --------------------------------------------------------------------------
PRAZO_DIAS = 7          # RN02 — prazo padrão de empréstimo
MULTA_POR_DIA = 1.00    # RN03 — R$ 1,00 por dia de atraso
LIMITE_LIVROS = 3       # RN01 — máximo de livros por aluno ao mesmo tempo


class Usuario(db.Model):
    """
    No diagrama de classes, Usuario é a classe-mãe de Aluno e Bibliotecario.
    Aqui a herança virou o campo 'perfil', que é como isso costuma ser feito
    no banco de dados quando as filhas não têm campos próprios.
    """
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    perfil = db.Column(db.String(20), nullable=False)   # 'aluno' ou 'bibliotecario'
    matricula = db.Column(db.String(20))

    emprestimos = db.relationship("Emprestimo", back_populates="aluno")

    def definir_senha(self, senha):
        # RNF02 — a senha é guardada criptografada, nunca em texto puro
        self.senha_hash = generate_password_hash(senha)

    def autenticar(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def e_bibliotecario(self):
        return self.perfil == "bibliotecario"

    def emprestimos_ativos(self):
        return [e for e in self.emprestimos if e.data_devolucao is None]

    def tem_multa_em_aberto(self):
        # RN06 — aluno devendo fica bloqueado
        return any(e.multa and e.multa.status == "Em aberto"
                   for e in self.emprestimos)

    def __repr__(self):
        return f"<Usuario {self.nome}>"


class Livro(db.Model):
    __tablename__ = "livro"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(120))
    editora = db.Column(db.String(120))
    categoria = db.Column(db.String(80))
    ano = db.Column(db.Integer)
    qtd_exemplares = db.Column(db.Integer, nullable=False, default=1)

    emprestimos = db.relationship("Emprestimo", back_populates="livro")

    def qtd_emprestados(self):
        return len([e for e in self.emprestimos if e.data_devolucao is None])

    def qtd_disponiveis(self):
        return self.qtd_exemplares - self.qtd_emprestados()

    def tem_disponivel(self):
        # RN08 — só empresta se sobrar exemplar
        return self.qtd_disponiveis() > 0

    def __repr__(self):
        return f"<Livro {self.titulo}>"


class Emprestimo(db.Model):
    __tablename__ = "emprestimo"

    id = db.Column(db.Integer, primary_key=True)
    data_retirada = db.Column(db.Date, nullable=False, default=date.today)
    data_prevista = db.Column(db.Date, nullable=False)
    data_devolucao = db.Column(db.Date)

    aluno_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    livro_id = db.Column(db.Integer, db.ForeignKey("livro.id"), nullable=False)

    aluno = db.relationship("Usuario", back_populates="emprestimos")
    livro = db.relationship("Livro", back_populates="emprestimos")
    multa = db.relationship("Multa", back_populates="emprestimo", uselist=False)

    # ---------------------------------------------------------------
    # A REGRA DE NEGÓCIO DO TRABALHO: cálculo da multa por atraso (RN03)
    # ---------------------------------------------------------------

    def dias_de_atraso(self, hoje=None):
        """Quantos dias passaram da data prevista. Zero se está em dia."""
        fim = self.data_devolucao or hoje or date.today()
        if fim <= self.data_prevista:
            return 0
        return (fim - self.data_prevista).days

    def calcular_multa(self, hoje=None):
        """R$ 1,00 por dia de atraso. Zero se não houve atraso."""
        return round(self.dias_de_atraso(hoje) * MULTA_POR_DIA, 2)

    def esta_atrasado(self, hoje=None):
        return self.dias_de_atraso(hoje) > 0

    def devolvido(self):
        return self.data_devolucao is not None

    def __repr__(self):
        return f"<Emprestimo {self.id}>"


class Multa(db.Model):
    __tablename__ = "multa"

    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Em aberto")
    data_pagamento = db.Column(db.Date)

    emprestimo_id = db.Column(db.Integer, db.ForeignKey("emprestimo.id"),
                              nullable=False)
    emprestimo = db.relationship("Emprestimo", back_populates="multa")

    def pagar(self):
        self.status = "Paga"
        self.data_pagamento = date.today()

    def __repr__(self):
        return f"<Multa {self.valor}>"


# ------------------------------------------------------------------ funções

def calcular_data_prevista(retirada=None):
    """RN02 — a devolução é 7 dias depois da retirada."""
    return (retirada or date.today()) + timedelta(days=PRAZO_DIAS)
