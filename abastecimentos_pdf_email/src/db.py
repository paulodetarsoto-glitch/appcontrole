from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///abastecimentos.db"  # Example database URL

Base = declarative_base()

class Abastecimento(Base):
    __tablename__ = 'abastecimentos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    placa = Column(String, nullable=False)
    justificativa = Column(String, nullable=False)
    supervisor = Column(String, nullable=False)
    setor = Column(String, nullable=False)
    quantidade_litros = Column(Float, nullable=False)
    tipo_combustivel = Column(String, nullable=False)

def get_db_session():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()