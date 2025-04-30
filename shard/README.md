# Setup

1. Make sure you have poetry installed

2. Install the requirements:
   ```
   poetry install
   ```

3. Run the module:
   - Master: 
   ```
   python -m shard --mode master --port {port} 
   ```
   - Slave:
   ```
   python -m shard --mode slave --port {port} --master-host {ip:port}
   ```
4. FastApi will be run on http://0.0.0.0:5050
5. Swagger: http://0.0.0.0:5050/docs


# Functional:

## Master:
1. Communicate with a user via http:
    - HTTP was chosen due to its popularity and convenience for handling stateful interactions and authentication.
    - Authentication (login, password, token)
    - GET/PUT secret - get or store secret
2. Communicate with Slaves via grpc
    - gRPC was selected as a fast and widely adopted protocol for efficient communication between internal services.
    - Accept connection request of new Slave
    - Get/Put parts
3. Use SSS to encrypt a secret
    - Our own package with Shamir's Secret Sharing algorithm for data encryption
4. Store the routing table for distribute parts of a secret between Slaves
    - Table to map user's secret to Slave nodes

## Slave:
1. Communicate with Master via grpc
2. Store parts of a secret

# Project organization
```
shard
├── __main__.py # Module entrypoint
├── master # Master module
├── slave # Slave module
└── resources # Protobuf generation
```