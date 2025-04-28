from shard.master.db.models.slave import Slave


class SlaveManager:
    def __init__(self, session):
        self.session = session

    def add(self, host: str) -> Slave:
        slave = Slave(host=host)
        self.session.add(slave)
        self.session.commit()
        return slave

