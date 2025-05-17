import configparser
from dataclasses import dataclass, field


@dataclass
class LoggingConfig:
    sqlalchemy_log_file: str = '/var/log/shard/app.log'
    log_level: str = 'INFO'


@dataclass
class AppConfig:
    args: str = '--mode master --port 8000'
    db_path: str = '/var/log/shard/master.db'
    logging: LoggingConfig = field(default_factory=LoggingConfig)


def read_config(config_path: None | str) -> AppConfig:
    if config_path:
        config = configparser.ConfigParser()

        if not config.read(config_path):
            raise FileNotFoundError(f"Cannot read config file: {config_path}")

        logging_cfg = LoggingConfig(
            sqlalchemy_log_file=config.get('logging', 'sqlalchemy_log_file', fallback='/var/log/shard/sqlalchemy.log'),
            log_level=config.get('logging', 'log_level', fallback='INFO'),
        )

        app_cfg = AppConfig(
            args=config.get('app', 'args', fallback='--mode master --port 8000'),
            db_path=config.get('app', 'db_path', fallback='/var/log/shard/master.db'),
            logging=logging_cfg,
        )
    else:
        app_cfg = AppConfig()

    return app_cfg
