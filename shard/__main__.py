import argparse
import asyncio
import sys
from pathlib import Path

import shard.master as master
import shard.slave as slave
from shard.config import read_config, AppConfig


class MainStarter:
    """
     - Parse args (from CLI or config)
     - Start appropriate mode
    """
    def start(self):
        mode, port, master_host, config = self.__parse_args()

        if mode == 'master':
            asyncio.run(self.__start_master(port, config.db_path, config.logging.sqlalchemy_log_file))
        elif mode == 'slave':
            self.__start_slave(master_host, port, config.db_path, config.logging.sqlalchemy_log_file)
        else:
            print('unknown mode')

    def __parse_args(self) -> tuple[str, int, str, AppConfig]:
        config_parser = argparse.ArgumentParser(add_help=False)
        config_parser.add_argument('--config', default=None)
        config_args, remaining_argv = config_parser.parse_known_args()

        cli_args = remaining_argv

        config = read_config(config_args.config)

        # If --config is specified, read arguments from config
        if config_args.config:
            cli_args = config.args.split()

        parser = argparse.ArgumentParser(description="SHamir Algorithm Reliable Distributed")

        parser.add_argument('--mode', choices=['master', 'slave'], required=True, help="Run mode: master or slave")
        parser.add_argument('--port', required=True, help="Grpc Server Port")
        parser.add_argument('--master-host', help="Master host address (required in slave mode)")

        args = parser.parse_args(cli_args)

        return str(args.mode), int(args.port), str(args.master_host), config

    async def __start_master(self, grpc_port: int, db_path, log_file):
        print("Starting in MASTER mode...")
        # TODO request http_port from user
        await master.start(db_path, log_file, 5050, grpc_port)

    def __start_slave(self, master_host: str, port: int, db_file, log_file):
        print("Starting in SLAVE mode...")
        slave.start(db_file, log_file, master_host, port)


if __name__ == '__main__':
    print("-- Shard --")

    MainStarter().start()
