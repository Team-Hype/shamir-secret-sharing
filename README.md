![Tests](https://github.com/Team-Hype/shamir-secret-sharing/actions/workflows/package-test.yaml/badge.svg)
![PYPI](https://img.shields.io/pypi/v/shamir_ss.svg)
![versions](https://img.shields.io/pypi/pyversions/shamir_ss.svg)
# Shamir Secret Sharing Project
| Deliverable | Status | Deployment/Implementation | Documentation |
|-------------|--------|---------------------------|---------------|
| Shamir crypto package (`shamir_ss`) | ✅ Published | [PyPI Package](https://pypi.org/project/shamir_ss/) | [README](package/README.md) |
| CLI Application | ✅ Implemented | [CLI Source](package/shamir_ss/__main__.py) | [README](package/README.md) |
| Shard Distributed Secret Vault | ✅ Implemented | [Shard Source](shard/) | [README](shard/README.md) |
| WebUI Demonstration | ✅ Deployed | [Web UI](https://aquaf1na.fun) | [README](client/README.md) |
| Online docs | 🚧 In process | ~ | ~ |

## Project Goals
### Core Components
 - [x] ~~Shamir crypto package~~
 - [x] ~~Shamir CLI Application~~
 - [x] ~~Shard Distributed Secret Vault Implementation~~
 - [x] ~~WebUI Demonstration~~

### Automation & CI/CD
 - [x] ~~Python package deployment~~
 - [x] ~~CI with Tests~~
 - [x] ~~Docker compose for Shard~~
 - [x] ~~Pre-commit linters & formatters~~

### Validation [checklist](requirements.md)
 - [x] ~~Hash the input and reconstructed secrets to confirm integrity~~
 - [x] ~~Attempt reconstruction with insufficient shares (should fail)~~
 - [x] ~~Log generation and reconstruction steps for auditability~~

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
