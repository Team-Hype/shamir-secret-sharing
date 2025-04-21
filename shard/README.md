# Overview. Python Server

## Functional:

Two modes:
1. Master
2. Slave

### Master:
1. Communicate with a user via http:
    - Authentication (login, password, token)
    - GET/PUT secret - get or store secret
2. Communicate with Slaves via grpc
    - Accept connection request of new Slave
    - Get/Put parts
3. Use SSS to encrypt a secret
    - Our own package with Shamir's Secret Sharing algorithm for data encryption
4. Store the routing table for distribute parts of a secret between Slaves
    - Table to map user's secret to Slave nodes

### Slave:
1. Communicate with Master via grpc
2. Store parts of a secret
