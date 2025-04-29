import grpc

import shard.resources.generated.master_pb2 as cf
import shard.resources.generated.master_pb2_grpc as cf_grpc


class MasterServer(cf_grpc.MasterServicer):

    def Connect(self, request: cf.ConnectionRequest, context: grpc.ServicerContext):
        # TODO pretty
        peer = context.peer()  # 'ipv4:127.0.0.1:50000'
        print(f"Client peer: {peer}")

        if peer.startswith('ipv4:'):
            ip_port = peer.split(':', 1)[1]
            ip, port = ip_port.rsplit(':', 1)
        else:
            ip, port = 'unknown', 'unknown'

        print(f"Client IP: {ip}, Port: {port}")

        from shard.master.db.managers import SlaveManager
        from shard.master.db import get_db
        slave_manager = SlaveManager(session=next(get_db()))
        slave_manager.add(ip)

        return cf.ConnectionResponse(approve=True)
