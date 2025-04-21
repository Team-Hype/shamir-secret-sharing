from concurrent import futures

import grpc

import shard.generated.slave_pb2 as cf
import shard.generated.slave_pb2_grpc as cf_grpc


class SlaveServer(cf_grpc.SlaveServicer):

    def PutSecretPart(self, request: cf.SecretPart, context: grpc.ServicerContext):
        pass

    def GetSecretPart(self, request: cf.Key, context: grpc.ServicerContext):
        pass


def start(port: str):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cf_grpc.add_SlaveServicer_to_server(SlaveServer(), server)

    server.add_insecure_port(f"0.0.0.0:{port}")
    print(f"Server started on port {port}")

    try:
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)
        print("\nServer stopped")
