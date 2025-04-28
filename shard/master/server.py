from concurrent import futures

import grpc

import shard.generated.master_pb2 as cf
import shard.generated.master_pb2_grpc as cf_grpc


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
        slave_manager = SlaveManager(session=get_db())
        slave_manager.add(ip)

        return cf.ConnectionResponse()

def start(port: str):
    import shamir_ss as sss
    a = sss.generate_shares(123, 3, 5)
    print(a)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cf_grpc.add_MasterServicer_to_server(MasterServer(), server)

    server.add_insecure_port(f"0.0.0.0:{port}")
    print(f"Server started on port {port}")

    try:
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)
        print("\nServer stopped")

