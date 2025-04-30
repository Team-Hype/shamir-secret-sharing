import grpc

import shard.resources.generated.master_pb2 as cf
import shard.resources.generated.master_pb2_grpc as cf_grpc


class MasterServer(cf_grpc.MasterServicer):

    def Connect(self, request: cf.ConnectionRequest, context: grpc.ServicerContext):
        # TODO pretty
        peer = context.peer()
        port = request.port

        if peer.startswith('ipv4:'):
            ip = peer.split(':')[1]
        else:
            ip = 'unknown'

        host = f"{ip}:{port}"

        print(f"Client host: {host}")

        from shard.master.db.managers import SlaveManager
        from shard.master.db import get_db

        slave_manager = SlaveManager(session=next(get_db()))

        if slave_manager.get(host) is None:
            slave_manager.add(f"{ip}:{port}")

        return cf.ConnectionResponse(approve=True)
