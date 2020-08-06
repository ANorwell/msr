import click
import os

from msr.registry import Registry
from msr.measurement import Measurement
from msr.version import library_version

base_dir = os.getenv('XDG_DATA_DIR', f"{os.getenv('HOME')}/.config")
registry = Registry.create(base_dir)

parallelism_config = 10

@click.group()
@click.option("-p", "--parallelism", default=10, type=int, show_default=True)
def cli(parallelism):
    """A tool for measuring URL response time."""
    global parallelism_config
    parallelism_config = parallelism
    pass

@cli.command()
def version():
    """Displays the version of the program"""
    click.echo(library_version())

@cli.command()
@click.argument('url')
def register(url):
    """Registers the provided URL"""
    click.secho(f"Registering {url}", fg="blue")
    registry.register(url)

@cli.command()
def list():
    """Lists all registered URLs"""
    click.secho("All registered URLs:", fg="blue", bold="True")
    for url in registry.list():
        click.echo(url)

@cli.command()
def measure():
    """Displays the size of each registered URL"""
    table(Measurement(parallelism_config).response_size(registry.list()))

@cli.command()
def response_times():
    """Displays the response time of each registered URL"""
    table(Measurement(parallelism_config).response_time(registry.list()))

@cli.command()
def race():
    """Displays the average response time by domain"""
    click.secho("Racing...", fg="blue", bold=True)
    table(Measurement(parallelism_config).average_response_time(registry.list()))

def table(column_pairs):
    for (name, value) in column_pairs:
        styled_name = click.style(name, bold=True)
        click.echo("{:50} {}".format(styled_name, value))