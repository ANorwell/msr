import click
import os

from msr.registry import Registry
from msr.version import library_version

base_dir = os.getenv('XDG_DATA_DIR', f"{os.getenv('HOME')}/.config")
registry = Registry.create(base_dir)

@click.group()
def cli():
    """A tool for measuring URL response time."""
    pass

@cli.command()
def version():
    """Displays the version of the program."""
    click.echo(library_version())

@cli.command()
@click.argument('url')
def register(url):
    "Registers the provided URL"
    click.echo(f"Registering {url}")
    registry.register(url)

@cli.command()
def list():
    click.echo("All registered URLs:")
    for url in registry.list():
        click.echo(url)

