from concurrent import futures

import grpc

import shard.resources.generated.master_pb2 as cf_master
import shard.resources.generated.master_pb2_grpc as cf_grpc_master
import shard.resources.generated.slave_pb2_grpc as cf_grpc
from shard.slave.db import init_database
from shard.slave.grpc.server import SlaveServer


def connect_to_master(master_host: str, self_port: int) -> bool:
    print(f"Connecting to Master at {master_host}")
    with grpc.insecure_channel(master_host) as channel:
        for i in range(5):
            stub = cf_grpc_master.MasterStub(channel)
            connected = stub.Connect(cf_master.ConnectionRequest(port=self_port))
            print(connected)
            if connected.approve:
                print(f"Connected to Master at {master_host}")
                return True
        else:
            print("Failed to connect to Master.")
            return False


def start(db_path, log_file, master_host: str, grpc_port: int):
    """
    Start Slave's gRPC server
    Connect to the Master
    """
    init_database(db_path, log_file)

    connected = connect_to_master(master_host, grpc_port)

    if not connected:
        return

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cf_grpc.add_SlaveServicer_to_server(SlaveServer(), server)

    server.add_insecure_port(f"0.0.0.0:{grpc_port}")
    print(f"Server started on port {grpc_port}")

    try:
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)
        print("\nServer stopped")
