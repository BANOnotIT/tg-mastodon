import logging
from pathlib import Path

import typer
from toml import loads

from .. import http

logging = logging.getLogger(__name__)


def get_channel_attr(config, channel: str, prop: str):
    if prop in config['channel'][channel]:
        return config['channel'][channel][prop]
    elif prop in config.get('default_attrs', {}):
        return config['default_attrs'][prop]
    else:
        raise ValueError(
            f'No {prop!r} found in {channel!r} channel or in default_attrs, but it\'s required')


def get_default_config():
    return str(Path(typer.get_app_dir('tg-mastodon')) / 'config.toml')


def get_default_logger_config():
    return str(Path(typer.get_app_dir('tg-mastodon')) / 'logger.toml')


def setup_config(ctx: typer.Context, config_path: Path):
    logging.info(f'Using config from {config_path.absolute()}')
    assert config_path.is_file(), 'asdf'
    config = loads(config_path.read_text())
    ctx.meta['config'] = config

    return config


class TapAsserter:
    counter = 0
    all_valid = True

    def check(self, cond: bool, text: str):
        self.counter += 1

        self.all_valid &= cond

        if cond:
            print(f'ok {self.counter} - {text}')
        else:
            print(f'not ok {self.counter} - {text}')

    def reset(self):
        self.counter = 0

    def stat(self):
        print(f'1..{self.counter}')
