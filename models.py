from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

"""
-- rodar este script em individual para criar o banco de dados e a(s) tabela(s);
$ python <este-arquivo>.py
"""

DB_URI = 'sqlite:///./main.db'
Base = declarative_base()

class Pedidos(Base):
    __tablename__ = 'pedidos'

    id = Column(Integer, primary_key=True)
    mesa = Column(String(200))
    andar = Column(String(200))
    pedidos = Column(String(1000))
    valor_pedidos = Column(String(1000))
    data = Column(String(80))
    hora = Column(String(80))

class Pagamento_pedidos(Base):
    __tablename__ = 'pagamento_pedidos'

    id = Column(Integer, primary_key=True)
    id_pedido = Column(String(200))
    tipo_de_pagamento = Column(String(200))
    valor = Column(String(200))
    data = Column(String(80))
    hora = Column(String(80))

if __name__ == "__main__":
    from sqlalchemy import create_engine

    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
