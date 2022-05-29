import logging
from logging import config as logging_configurator, INFO
from datetime import datetime, timedelta
from pathlib import Path

import typer
from toml import loads

from .utils import get_default_config, get_channel_attr, setup_config, get_default_logger_config
from .config import config_app

app = typer.Typer()
app.add_typer(config_app, name='config')
log = logging.getLogger(__name__)


@app.callback()
def main(
        ctx: typer.Context,
        config_path: Path = typer.Option(
            get_default_config,
            resolve_path=True,
        ),
        logger_config: Path = typer.Option(
            get_default_logger_config,
            resolve_path=True,
        ),
):
    ctx.meta['config_path'] = config_path

    if logger_config.exists():
        if logger_config.suffix == '.toml':
            conf = loads(logger_config.read_text())
            logging_configurator.dictConfig(conf)
        elif logger_config.suffix == '.ini':
            logging_configurator.fileConfig(str(logger_config))
    else:
        logging.basicConfig(level=INFO)
        log.info('Using default logger config')


@app.command(help='Repost posts from telegram channel')
def repost(ctx: typer.Context,
           channel: str = typer.Argument(...,
                                         help='The name for the channel, specified in config file'),
           dry: bool = typer.Option(False,
                                    help='Use log entries instead of uploading them to redmine')):
    config = setup_config(ctx, ctx.meta['config_path'])
