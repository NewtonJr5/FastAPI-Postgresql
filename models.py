from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Maquina(Base):
    __tablename__ = 'maquinas'  # Nome da tabela corrigido
    
    codigo = Column(Integer, primary_key=True, index=True, autoincrement=True)
    funcao = Column(String, index=True)

    # Relacionamento com a tabela de manutenção de máquina
    manutencoes = relationship("Manutencao_maquina", back_populates="maquina")


class Manutencao_maquina(Base):
    __tablename__ = 'manutencao_maquina'

    manutencao_codigo_manutencao = Column(Integer, ForeignKey('manutencao.codigo_manutencao'), primary_key=True)
    maquina_codigo = Column(Integer, ForeignKey('maquinas.codigo'), primary_key=True)
    data_inicio = Column(String)
    data_fim = Column(String)

    # Relacionamento com as tabelas Maquina e Manutencao
    maquina = relationship("Maquina", back_populates="manutencoes")
    manutencao = relationship("Manutencao", back_populates="manutencoes_maquina")


class Manutencao(Base):
    __tablename__ = 'manutencao'

    codigo_manutencao = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String)

    # Relacionamento com a tabela de manutenção de máquina
    manutencoes_maquina = relationship("Manutencao_maquina", back_populates="manutencao")
