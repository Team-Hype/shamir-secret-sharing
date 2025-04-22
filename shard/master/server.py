from concurrent import futures

import grpc

import shard.generated.master_pb2 as cf
import shard.generated.master_pb2_grpc as cf_grpc


class MasterServer(cf_grpc.MasterServicer):

    def Connect(self, request: cf.ConnectionRequest, context: grpc.ServicerContext):
        pass


def start(port: str):
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
