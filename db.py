import datetime
from sqlalchemy import Column, String, Integer, Date, create_engine
from sqlalchemy.orm import declarative_base, relationship, declared_attr, sessionmaker
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()


class Parametro(Base):
    __tablename__ = 'parametri'

    id = Column(Integer, primary_key=True, autoincrement=True)
    valido_dal = Column(Date, nullable=False, unique=True)
    costo_scale = Column(Integer)
    pulizie_al_mese = Column(Integer)
    quota_mensile = Column(Integer)

    def __repr__(self) -> str:
        return "<Parametro(id=%d, data=%s, costo_scale=%d, pulizie_al_mese=%d, quota_mensile=%d)>" % (
            self.id, self.data, self.costo_scale,
            self.pulizie_al_mese, self.quota_mensile)


class Condomino(Base):
    __tablename__ = 'condomini'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    versamenti_quote = relationship(
        "VersamentoQuote", back_populates="condomino")

    def __repr__(self) -> str:
        return "<Condomino(id=%d, nome='%s')>" % (self.id, self.nome)


class Operazione(Base):
    __tablename__ = 'operazioni'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date, nullable=False)
    importo = Column(Integer, nullable=False)
    type = Column(String(20))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'operazione'
    }


class PagamentoScale(Operazione):
    __mapper_args__ = {
        'polymorphic_identity': 'pagamento_scale'
    }


class VersamentoQuote(Operazione):
    condomino_id = Column(Integer, ForeignKey('condomini.id'))
    condomino = relationship("Condomino", back_populates="versamenti_quote")

    __mapper_args__ = {
        'polymorphic_identity': 'versamento_quote'
    }


class AltraSpesa(Operazione):
    __mapper_args__ = {
        'polymorphic_identity': 'altra_spesa'
    }

    @declared_attr
    def causale(cls):
        "Causale column, if not present already."
        return Operazione.__table__.c.get('causale', Column(String))


class AltroVersamento(Operazione):
    __mapper_args__ = {
        'polymorphic_identity': 'altro_versamento'
    }

    @declared_attr
    def causale(cls):
        "Causale column, if not present already."
        return AltraSpesa.__table__.c.get('causale', Column(String))


class Prestito(Operazione):
    __mapper_args__ = {
        'polymorphic_identity': 'prestito'
    }


class Restituzione(Operazione):
    __mapper_args__ = {
        'polymorphic_identity': 'restituzione'
    }


engine = create_engine('sqlite:///stato_scale.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(engine)
session = Session()


def setup():
    if session.query(Parametro).count() == 0:
        parametro_iniziale = Parametro(
            valido_dal=datetime.datetime(year=2019, month=7, day=1).date(),
            costo_scale=20,
            pulizie_al_mese=2,
            quota_mensile=12)
        session.add(parametro_iniziale)

    if session.query(Condomino).count() == 0:
        session.add_all([
            Condomino(id=0, nome="Michela"),
            Condomino(id=1, nome="Gerardo"),
            Condomino(id=2, nome="Elena"),
            Condomino(id=3, nome="Giulia")])

    session.commit()
