from concurrent import futures

import grpc

import shard.resources.generated.slave_pb2_grpc as cf_grpc
from shard.slave.grpc.server import SlaveServer


def start(master_host: str, port: str):
    # print(f"Connecting to Master at {master_host}") TODO Connect

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
