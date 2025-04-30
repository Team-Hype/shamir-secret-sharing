![Tests](https://github.com/Team-Hype/shamir-secret-sharing/actions/workflows/package-test.yaml/badge.svg)
![PYPI](https://img.shields.io/pypi/v/shamir_ss.svg)
![versions](https://img.shields.io/pypi/pyversions/shamir_ss.svg)
# Shamir Secret Sharing Project
## Project Goals
### Core Components
 - [x] ~~Shamir crypto package~~
 - [x] ~~Shamir CLI Application~~
 - [ ] Shard Distributed Secret Vault Implementation
 - [x] ~~WebUI Demonstration~~

### Automation & CI/CD
 - [x] ~~Python package deployment~~
 - [x] ~~CI with Tests~~
 - [ ] Docker compose for Shard
 - [x] ~~Pre-commit linters & formatters~~

### Validation [checklist](requirements.md)
 - [x] ~~Hash the input and reconstructed secrets to confirm integrity~~
 - [x] ~~Attempt reconstruction with insufficient shares (should fail)~~
 - [ ] Log generation and reconstruction steps for auditability

## Project organization
```
.
├── client  # Web client 
├── package # Crypto package
└── shard   # Distributed secret vault
```

## Shard Architecture Scheme
![Shard Architecture Scheme](/images/shard-scheme.png)

## References & Resources
- [Original Shamir Paper](https://web.mit.edu/6.857/OldStuff/Fall03/ref/Shamir-HowToShareASecret.pdf)
- [Shamir's Secret Sharing Wikipedia](https://en.wikipedia.org/wiki/Shamir%27s_secret_sharing)
- [Interactive Shamir Web Demo](https://iancolechen.io/shamir/)
- [Secret Sharing Explained Visually](https://www.youtube.com/watch?v=iFY5SyY3IMQ)
