import argparse
import sys

import shard.slave as slave
import shard.master as master

def start_master(port: str):
    print("Starting in MASTER mode...")
    master.start(port)

def start_slave(master_host, port):
    print("Starting in SLAVE mode...")
    slave.start(master_host, port=port)

if __name__ == '__main__':
    print("-- Shard --")

    parser = argparse.ArgumentParser(description="SHamir Algorithm Reliable Distributed")

    parser.add_argument('--mode', choices=['master', 'slave'], required=True, help="Run mode: master or slave")
    parser.add_argument('--port', required=True, help="Grpc Server Port")
    parser.add_argument('--master-host', help="Master host address (required in slave mode)")

    args = parser.parse_args()

    if args.mode == 'master':
        if args.master_host:
            print("Error: --master-host should not be used in master mode.")
            sys.exit(1)
        start_master(args.port)
    elif args.mode == 'slave':
        if not args.master_host:
            print("Error: --master-host is required in slave mode.")
            sys.exit(1)
        start_slave(args.master_host, args.port)



