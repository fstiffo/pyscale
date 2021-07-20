import datetime
from sqlalchemy import Column, String, Integer, Date, create_engine, text, select
from sqlalchemy.orm import declarative_base, relationship, declared_attr, sessionmaker, with_polymorphic
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

    def contabile(self):
        return self.importo

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'operazione'
    }


class PagamentoScale(Operazione):

    def contabile(self):
        return -self.importo

    def __str__(self) -> str:
        return "Pagamento scale"

    __mapper_args__ = {
        'polymorphic_identity': 'pagamento_scale'
    }


class VersamentoQuote(Operazione):
    condomino_id = Column(Integer, ForeignKey('condomini.id'))
    condomino = relationship("Condomino", back_populates="versamenti_quote")

    def __str__(self) -> str:
        return f"Pagamento quote ({self.condomino.nome})"

    __mapper_args__ = {
        'polymorphic_identity': 'versamento_quote'
    }


class AltraSpesa(Operazione):

    def contabile(self):
        return -self.importo

    @declared_attr
    def causale(cls):
        """Causale column, if not present already."""
        return Operazione.__table__.c.get('causale', Column(String))

    def __str__(self) -> str:
        return f"Altra spesa ({self.causale})"

    __mapper_args__ = {
        'polymorphic_identity': 'altra_spesa'
    }


class AltroVersamento(Operazione):
    @declared_attr
    def causale(cls):
        """Causale column, if not present already."""
        return AltraSpesa.__table__.c.get('causale', Column(String))

    def __str__(self) -> str:
        return f"Altro versamento ({self.causale})"

    __mapper_args__ = {
        'polymorphic_identity': 'altro_versamento'
    }


class Prestito(Operazione):
    def contabile(self):
        return -self.importo

    def __str__(self) -> str:
        return f"Prestito"

    __mapper_args__ = {
        'polymorphic_identity': 'prestito'
    }


class Restituzione(Operazione):
    def __str__(self) -> str:
        return f"Restituzione"

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


def import_from_scale():
    engine_scale = create_engine('sqlite:///scale.db', echo=True)

    with engine_scale.connect() as connection:
        result = connection.execute(text("SELECT * FROM PulizieScale"))
        for row in result:
            pagamento_scale = PagamentoScale(
                data=datetime.datetime(
                    year=int(row['anno']),
                    month=int(row['mese']),
                    day=int(row['giorno'])),
                importo=20)
            session.add(pagamento_scale)

        result = connection.execute(text("SELECT * FROM VersamentiQuote"))
        for row in result:
            versamento_quote = VersamentoQuote(
                data=datetime.datetime(
                    year=int(row['anno']),
                    month=int(row['mese']),
                    day=int(row['giorno'])),
                importo=int(row['importo']),
                condomino_id=int(row['id_condomino']))
            session.add(versamento_quote)

        result = connection.execute(text("SELECT * FROM AltreSpese"))
        for row in result:
            altra_spesa = AltraSpesa(
                data=datetime.datetime(
                    year=int(row['anno']),
                    month=int(row['mese']),
                    day=int(row['giorno'])),
                importo=int(row['importo']),
                causale=row['descrizione'])
            session.add(altra_spesa)

        result = connection.execute(text("SELECT * FROM AltriVersamenti"))
        for row in result:
            altro_versamento = AltroVersamento(
                data=datetime.datetime(
                    year=int(row['anno']),
                    month=int(row['mese']),
                    day=int(row['giorno'])),
                importo=int(row['importo']),
                causale=row['descrizione'])
            session.add(altro_versamento)

        result = connection.execute(text("SELECT * FROM Prestiti_"))
        for row in result:
            prestito = Prestito(
                data=datetime.datetime(
                    year=int(row['anno']),
                    month=int(row['mese']),
                    day=int(row['giorno'])),
                importo=int(row['importo']))
            session.add(prestito)

        result = connection.execute(text("SELECT * FROM Restituzioni_"))
        for row in result:
            restituzione = Restituzione(
                data=datetime.datetime(
                    year=int(row['anno']),
                    month=int(row['mese']),
                    day=int(row['giorno'])),
                importo=int(row['importo']))
            session.add(restituzione)

    session.commit()


def nome_condomino(condomino_id):
    stmt = select(Condomino).where(Condomino.id == condomino_id)
    result = session.execute(stmt)
    return result.scalars().first().nome


def cassa():
    # query using with_polymorphic.
    operazione_subclasses = with_polymorphic(Operazione,
                                             [PagamentoScale, VersamentoQuote, AltraSpesa, AltroVersamento, Prestito,
                                              Restituzione])
    stmt = select(operazione_subclasses)
    result = session.execute(stmt)
    return sum(map(lambda o: o.contabile(), result.scalars().all()))


def get_operazioni():
    # query using with_polymorphic.
    operazione_subclasses = with_polymorphic(Operazione,
                                             [PagamentoScale, VersamentoQuote, AltraSpesa, AltroVersamento, Prestito,
                                              Restituzione])
    stmt = select(operazione_subclasses).order_by(Operazione.data.desc())
    result = session.execute(stmt)
    return list(map(lambda o: [o.data.strftime("%d-%m-%Y"), o.contabile(), str(o)], result.scalars().all()))
