import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = orm.declarative_base()

_scoped_session = None


def global_init(db_file):
    global _scoped_session

    if _scoped_session:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False, pool_pre_ping=True)
    _scoped_session = orm.scoped_session(orm.sessionmaker(bind=engine))

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    if not _scoped_session:
        raise RuntimeError("База не инициализирована (вызов global_init)")
    return _scoped_session()


def remove_session():
    """Закрыть сессию текущего потока и вернуть соединение в пул (вызывать из teardown Flask)."""
    if _scoped_session is not None:
        _scoped_session.remove()
