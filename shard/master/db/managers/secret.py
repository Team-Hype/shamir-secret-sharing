from shard.master.db.models.secret import Secret
from shard.master.db.models.slave import Slave


class SecretManager:
    def __init__(self, session):
        self.session = session

    def add(self, key: str, hash_: str, required_parts: int) -> Secret:
        secret = Secret(key=key, hash=hash_, required_parts=required_parts)
        self.session.add(secret)
        self.session.commit()
        return secret

    def get(self, secret_id: int) -> Secret | None:
        return self.session.query(Secret).filter_by(id=secret_id).first()

    def get_by_key(self, key: str) -> Secret | None:
        return self.session.query(Secret).filter_by(key=key).first()

    def assign_slave(self, secret_id: int, slave_id: int):
        secret = self.get(secret_id)
        slave = self.session.query(Slave).filter_by(id=slave_id).first()
        if secret and slave:
            secret.slaves.append(slave)
            self.session.commit()
