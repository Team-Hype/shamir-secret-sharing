from shard.slave.db.models.secret import Secret

class SecretManager:
    def __init__(self, session):
        self.session = session

    def save(self, key: str, part: str):
        secret = self.session.query(Secret).filter_by(key=key).first()
        if secret:
            secret.part = part
        else:
            secret = Secret(key=key, part=part)
            self.session.add(secret)
        self.session.commit()
        return secret

    def get(self, key: str) -> Secret | None:
        return self.session.query(Secret).filter_by(key=key).first()
