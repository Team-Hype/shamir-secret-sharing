import base64

import grpc
import shamir_ss as sss
import pickle

from shard.master.db import get_db
from shard.master.db.managers import SlaveManager

import shard.resources.generated.slave_pb2 as cf
import shard.resources.generated.slave_pb2_grpc as cf_grpc


async def store_key(user_id: str, key: str, value: str, k: int = 2, n: int = 3) -> bool:
    """
    1. Apply shamir algorithm
    2. Encode share parts to strings
    3. Shuffle all slaves
    4. In for loop try to store part in slave
    5. Store mapping Slave-Part in DB
    """
    shares: list[tuple] = sss.generate_shares(value, 2, 3)
    encoded_shares = [encode_share(share) for share in shares]

    slave_manager = SlaveManager(next(get_db()))
    slaves = slave_manager.get_all()
    slaves = slaves  # shufle random

    success_slaves = []

    key = cf.Key(key=key)
    for slave in slaves:
        # All parts in are slaves
        if len(success_slaves) == n: break

        part_to_save = encoded_shares[0]

        with grpc.insecure_channel(slave.host) as channel:
            stub = cf_grpc.SlaveStub(channel)
            part = cf.SecretPart(key=key, part=part_to_save)
            # Try to store
            try:
                result = stub.PutSecretPart(part)
            except Exception as e:
                print(e)
                result = None

            if result:
                encoded_shares = encoded_shares[1:]
                success_slaves += [slave]

    if len(success_slaves) != n:
        return False


    # TODO store mapp in db

    return True


async def get_key(user_id: str, key: str) -> str:
    pass


def encode_share(share: tuple) -> str:
    pickled = pickle.dumps(share)  # bytes
    return base64.b64encode(pickled).decode("utf-8")


def decode_share(encoded: str) -> tuple:
    pickled = base64.b64decode(encoded.encode("utf-8"))
    return pickle.loads(pickled)
