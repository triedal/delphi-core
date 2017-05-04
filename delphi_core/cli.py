"""CLI module."""

import click
import logging
from feature_miner import PEMiner
from classifier import Classifier


logging.basicConfig(level=logging.DEBUG)

@click.group()
def cli():
    """The CLI for delphi-core."""

@cli.command()
@click.argument('mal_dir', type=click.Path(exists=True))
@click.argument('ben_dir', type=click.Path(exists=True))
def mine(mal_dir, ben_dir):
    """Mine PE files and save features to CSV file."""
    miner = PEMiner()
    miner.mine_features_to_csv(mal_dir, ben_dir)

@cli.command()
@click.argument('f', type=click.Path(exists=True))
def upload(f):
    """Uploads features from CSV file to SQL db."""
    miner = PEMiner()
    miner.save_csv_to_db(f)

@cli.command()
def train():
    """Trains classifier and exports model to file."""
    Classifier(train=True)



if __name__ == "__main__":
    cli()
