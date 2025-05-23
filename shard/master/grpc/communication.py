import base64
import hashlib
import pickle

import grpc
import shamir_ss as sss

import shard.resources.generated.slave_pb2 as cf
import shard.resources.generated.slave_pb2_grpc as cf_grpc
from shard.master.db import get_db
from shard.master.db.managers import SecretManager
from shard.master.db.managers import SlaveManager


# TODO rename to store_secret
async def store_key(user_id: str, key: str, value: str, k: int = 2, n: int = 3) -> bool:
    """
    1. Apply shamir algorithm
    2. Encode share parts to strings
    3. Shuffle all slaves
    4. In for loop try to store part in slave
    5. Store mapping Slave-Part in DB
    """
    # TODO split code
    shares: list[tuple] = sss.generate_text_shares(value, 2, 3)
    encoded_shares = [encode_share(share) for share in shares]

    slave_manager = SlaveManager(next(get_db()))
    slaves = slave_manager.get_all()
    slaves = slaves  # shufle random

    success_slaves = []

    for slave in slaves:
        # All parts in are slaves
        if len(success_slaves) == n: break

        part_to_save = encoded_shares[0]

        with grpc.insecure_channel(slave.host) as channel:
            stub = cf_grpc.SlaveStub(channel)
            part = cf.SecretPart(key=cf.Key(key=key), part=part_to_save)
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
        # TODO remove parts from slave
        return False

    secret_manager = SecretManager(next(get_db()))
    secret = secret_manager.add(key, take_hash(value), k)
    for slave in success_slaves:
        secret_manager.assign_slave(secret.id, slave.id)

    return True


# TODO rename to get_secret
async def get_key(user_id: str, key: str) -> str:
    """
    1. Get secret from db
    2. Get Slaves of this secret
    3. Request 'required_parts' number of Slaves for parts
    4. Reconstruct and return secret
    """
    # TODO split code
    session = next(get_db())
    secret_manager = SecretManager(session)

    secret = secret_manager.get_by_key(key)
    if not secret:
        raise ValueError("Secret not found")

    assigned_slaves = secret.slaves
    if len(assigned_slaves) < secret.required_parts:
        raise ValueError("Not enough shares to recover the secret")

    shares = []
    for slave in assigned_slaves:
        if len(shares) == secret.required_parts:
            break
        try:
            with grpc.insecure_channel(slave.host) as channel:
                stub = cf_grpc.SlaveStub(channel)
                response = stub.GetSecretPart(cf.Key(key=key))
                shares.append(decode_share(response.part))
        except Exception as e:
            print(f"Failed to get share from {slave.host}: {e}")

    if len(shares) < secret.required_parts:
        raise ValueError("Failed to retrieve enough shares")

    secret = sss.reconstruct_text_secret(shares)
    return secret


def take_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def encode_share(share: tuple) -> str:
    pickled = pickle.dumps(share)  # bytes
    return base64.b64encode(pickled).decode("utf-8")


def decode_share(encoded: str) -> tuple:
    pickled = base64.b64decode(encoded.encode("utf-8"))
    return pickle.loads(pickled)
