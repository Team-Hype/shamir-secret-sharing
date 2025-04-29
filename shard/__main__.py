import argparse
import asyncio

import shard.master as master
import shard.slave as slave


class MainStarter:
    """
     - Parse args
     - Start appropriate mode
    """
    def start(self):
        mode, port, master_host = self.__parse_args()

        if mode == 'master':
            asyncio.run(self.__start_master(port))
        elif mode == 'slave':
            self.__start_slave(master_host, port)
        else:
            print('unknown mode')

    def __parse_args(self) -> (str, int, str):
        parser = argparse.ArgumentParser(description="SHamir Algorithm Reliable Distributed")

        parser.add_argument('--mode', choices=['master', 'slave'], required=True, help="Run mode: master or slave")
        parser.add_argument('--port', required=True, help="Grpc Server Port")
        parser.add_argument('--master-host', help="Master host address (required in slave mode)")

        args = parser.parse_args()

        return args.mode, int(args.port), args.master_host

    async def __start_master(self, grpc_port: int):
        print("Starting in MASTER mode...")
        # TODO request http_port from user
        await master.start(5050, grpc_port)

    def __start_slave(self, master_host: str, port: int):
        print("Starting in SLAVE mode...")
        slave.start(master_host, port)


if __name__ == '__main__':
    print("-- Shard --")

    MainStarter().start()
