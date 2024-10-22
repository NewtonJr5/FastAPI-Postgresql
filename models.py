from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Maquina(Base):
    __tablename__ = 'maquina'  # Tabela agora é 'maquina'
    
    codigo = Column(Integer, primary_key=True, index=True, autoincrement=True)
    funcao = Column(String, index=True)
    manutencao = relationship("Manutencao_maquina", back_populates="maquina")


class Manutencao_maquina(Base):
    __tablename__ = 'manutencao_maquina'

    manutencao_codigo_manutencao = Column(Integer, ForeignKey('manutencao.codigo_manutencao'), primary_key=True)
    maquina_codigo = Column(Integer, ForeignKey('maquina.codigo'), primary_key=True)
    data_inicio = Column(String)
    data_fim = Column(String)
    maquina = relationship("Maquina", back_populates="manutencao")
    manutencao = relationship("Manutencao", back_populates="manutencao_maquinas")


class Manutencao(Base):
    __tablename__ = 'manutencao'

    codigo_manutencao = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String)
    manutencao_maquinas = relationship("Manutencao_maquina", back_populates="manutencao")

