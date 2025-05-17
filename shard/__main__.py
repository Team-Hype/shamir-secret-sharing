import argparse
import asyncio
import sys
from pathlib import Path

import shard.master as master
import shard.slave as slave


class MainStarter:
    """
     - Parse args (from CLI or config)
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
        config_parser = argparse.ArgumentParser(add_help=False)
        config_parser.add_argument('--config', default=None)
        config_args, remaining_argv = config_parser.parse_known_args()

        cli_args = remaining_argv

        # If --config is specified, read arguments from config
        if config_args.config:
            config_path = Path(config_args.config)
            if not config_path.exists():
                print(f"Config file {config_path} not found.")
                sys.exit(1)
            with open(config_path) as f:
                config_line = f.read().strip()
                cli_args = config_line.split()

        parser = argparse.ArgumentParser(description="SHamir Algorithm Reliable Distributed")

        parser.add_argument('--mode', choices=['master', 'slave'], required=True, help="Run mode: master or slave")
        parser.add_argument('--port', required=True, help="Grpc Server Port")
        parser.add_argument('--master-host', help="Master host address (required in slave mode)")

        args = parser.parse_args(cli_args)

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
