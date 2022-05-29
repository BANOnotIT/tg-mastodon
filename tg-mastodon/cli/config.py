import logging as logging
from pathlib import Path

import typer
from schema import SchemaError
from toml import loads, TomlDecodeError

from ..config import config_schema
from .utils import TapAsserter

config_app = typer.Typer()
logging = logging.getLogger(__name__)


@config_app.command()
def validate(ctx: typer.Context):
    tap = TapAsserter()

    path: Path = ctx.meta['config_path']
    tap.check(path.is_file(), f'Using config from {path}')

    config = path.read_text()
    tap.check(len(config) > 0, f'Config is not empty')

    valid = True
    try:
        config = loads(config)
    except TomlDecodeError as e:
        valid = False
        logging.exception(str(e))

    tap.check(valid, f'Config is valid toml')

    valid = True
    try:
        config_schema.validate(config)
    except SchemaError as e:
        valid = False
        logging.exception(str(e))
    tap.check(valid, 'Config is valid against Schema')

    tap.stat()

    if not tap.all_valid:
        exit(1)
