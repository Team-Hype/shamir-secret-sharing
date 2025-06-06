import asyncio
import signal

import grpc
import uvicorn

import shard.resources.generated.master_pb2_grpc as cf_grpc
from shard.master.db import init_database
from shard.master.grpc.server import MasterServer


async def start_grpc_server(port: int, stop_event: asyncio.Event):
    server = grpc.aio.server()
    cf_grpc.add_MasterServicer_to_server(MasterServer(), server)

    listen_addr = f"0.0.0.0:{port}"
    server.add_insecure_port(listen_addr)
    print(f"gRPC server started on {listen_addr}")

    await server.start()

    await stop_event.wait()

    print("Shutting down gRPC server...")
    await server.stop(0)


async def start_fastapi_server(port: int, stop_event: asyncio.Event):
    from shard.master.http import app

    config = uvicorn.Config(app=app, host="0.0.0.0", port=port, loop="asyncio", lifespan="off")
    server = uvicorn.Server(config)

    server_task = asyncio.create_task(server.serve())

    await stop_event.wait()
    print("Shutting down FastAPI server...")
    server.should_exit = True

    await server_task


async def start(db_path, log_file, http_port: int = 8000, grpc_port: int = 50051):
    """
     - Create stop asyncio event
     - Start gRPC and HTTP server.
    """
    init_database(db_path, log_file)

    stop_event = asyncio.Event()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop_event.set)

    grpc_task = asyncio.create_task(start_grpc_server(grpc_port, stop_event))
    fastapi_task = asyncio.create_task(start_fastapi_server(http_port, stop_event))

    await asyncio.gather(grpc_task, fastapi_task)
