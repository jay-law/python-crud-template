import logging
import logging.config
from pathlib import PurePath

import click

from crud.commands.factory import CmdFactory
from crud.config import configure_app

logger = logging.getLogger(__name__)


def configure_logging(log_level: str) -> None:
    log_level = "INFO" if log_level is None else log_level

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


@click.group
@click.option("-v", "--verbose", "log_level", flag_value="DEBUG")
@click.option("-q", "--quiet", "log_level", flag_value="CRITICAL")
@click.option("-e", "--environment", "env_file", type=PurePath)
@click.pass_context
def cli(ctx: click.Context, log_level: str, env_file: PurePath) -> None:
    if env_file is not None:
        configure_app(env_file)

    configure_logging(log_level)

    # params made available to cli.commands
    ctx.ensure_object(dict)
    ctx.obj["some_key"] = "some_value"

    pass


@cli.command()
@click.pass_context
def create(ctx: click.Context) -> None:
    x = ctx.obj["some_key"]
    logger.info(f"some_key value: {x}")
    cmd = CmdFactory.generate_command(cmd="create")
    cmd.validate_config()
    cmd.execute()


@cli.command()
@click.pass_context
@click.option("-f", "--file", "file", type=PurePath)
def read(ctx: click.Context, file: PurePath) -> None:
    cmd = CmdFactory.generate_command(cmd="read")
    cmd.validate_config()
    cmd.execute()
    cmd.read(file)  # type: ignore [union-attr]


@cli.command()
@click.pass_context
def update(ctx: click.Context) -> None:
    cmd = CmdFactory.generate_command(cmd="update")
    cmd.validate_config()
    cmd.execute()


@cli.command()
@click.pass_context
def delete(ctx: click.Context) -> None:
    cmd = CmdFactory.generate_command(cmd="delete")
    cmd.validate_config()
    cmd.execute()


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
