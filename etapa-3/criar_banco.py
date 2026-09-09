"""
Cria o banco de dados e coloca alguns dados de exemplo.

Rode uma vez antes de usar o sistema:   python criar_banco.py

Cria de propósito um empréstimo já atrasado, para dar para demonstrar o
cálculo da multa na apresentação sem precisar esperar uma semana.
"""
from datetime import date, timedelta

from app import app
from models import Emprestimo, Livro, Usuario, db

LIVROS = [
    ("Engenharia de Software", "Ian Sommerville", "Pearson",
     "Engenharia de Software", 2018, 3),
    ("UML 2 - Uma Abordagem Prática", "Gilleanes Guedes", "Novatec",
     "Engenharia de Software", 2018, 2),
    ("Sistemas de Banco de Dados", "Elmasri e Navathe", "Pearson",
     "Banco de Dados", 2011, 2),
    ("Introdução a Sistemas de Banco de Dados", "C. J. Date", "Elsevier",
     "Banco de Dados", 2004, 1),
    ("Algoritmos - Teoria e Prática", "Cormen", "LTC",
     "Programação", 2012, 2),
    ("Código Limpo", "Robert C. Martin", "Alta Books",
     "Programação", 2009, 1),
    ("Redes de Computadores", "Andrew Tanenbaum", "Pearson",
     "Redes", 2011, 2),
    ("Cálculo - Volume 1", "James Stewart", "Cengage",
     "Matemática", 2013, 4),
]

USUARIOS = [
    ("Maria Souza", "maria@uems.br", "bibliotecario", None),
    ("Carlos Lima", "carlos@uems.br", "bibliotecario", None),
    ("João Pedro Recalcatti", "joao@uems.br", "aluno", "2023001"),
    ("Sidney Alves Junior", "sidney@uems.br", "aluno", "2023002"),
    ("Ana Clara Dias", "ana@uems.br", "aluno", "2023003"),
]


def criar():
    with app.app_context():
        db.drop_all()
        db.create_all()

        for nome, email, perfil, matricula in USUARIOS:
            u = Usuario(nome=nome, email=email, perfil=perfil, matricula=matricula)
            u.definir_senha("123")
            db.session.add(u)

        for titulo, autor, editora, categoria, ano, qtd in LIVROS:
            db.session.add(Livro(titulo=titulo, autor=autor, editora=editora,
                                 categoria=categoria, ano=ano,
                                 qtd_exemplares=qtd))
        db.session.commit()

        joao = Usuario.query.filter_by(email="joao@uems.br").first()
        ana = Usuario.query.filter_by(email="ana@uems.br").first()
        codigo_limpo = Livro.query.filter_by(titulo="Código Limpo").first()
        cormen = Livro.query.filter_by(
            titulo="Algoritmos - Teoria e Prática").first()

        # empréstimo em dia: pego hoje, vence daqui a 7 dias
        db.session.add(Emprestimo(
            aluno=joao, livro=cormen,
            data_retirada=date.today(),
            data_prevista=date.today() + timedelta(days=7)))

        # empréstimo ATRASADO em 5 dias: serve para demonstrar a multa
        db.session.add(Emprestimo(
            aluno=ana, livro=codigo_limpo,
            data_retirada=date.today() - timedelta(days=12),
            data_prevista=date.today() - timedelta(days=5)))

        db.session.commit()

        print("Banco criado com sucesso.")
        print(f"  {Usuario.query.count()} usuários")
        print(f"  {Livro.query.count()} livros")
        print(f"  {Emprestimo.query.count()} empréstimos "
              "(um deles com 5 dias de atraso, para testar a multa)")
        print()
        print("Entrar como bibliotecário:  maria@uems.br / 123")
        print("Entrar como aluno:          joao@uems.br  / 123")


if __name__ == "__main__":
    criar()
