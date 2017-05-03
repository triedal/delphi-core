"""CLI module."""

import click
import logging
from feature_miner import PEMiner


logging.basicConfig(level=logging.DEBUG)

@click.group()
def cli():
    """The CLI for delphi-core."""

@cli.command()
def mine():
    """Mine PE files and save features to CSV file."""
    miner = PEMiner()
    miner.mine_features_to_csv()

@cli.command()
@click.argument('f', type=click.Path(exists=True))
def upload(f):
    """Uploads features from CSV file to SQL db."""
    miner = PEMiner()
    miner.save_csv_to_db(f)

if __name__ == "__main__":
    cli()
