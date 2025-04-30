from sqlalchemy.orm.exc import NoResultFound

from shard.master.db.models.slave import Slave


class SlaveManager:
    def __init__(self, session):
        self.session = session

    def add(self, host: str) -> Slave:
        slave = Slave(host=host)
        self.session.add(slave)
        self.session.commit()
        return slave

    def get(self, host: str) -> Slave | None:
        try:
            return self.session.query(Slave).filter_by(host=host).one()
        except NoResultFound:
            return None

    def get_all(self) -> list[Slave]:
        return self.session.query(Slave).all()
