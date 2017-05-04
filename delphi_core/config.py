"""
This module builds the globally accessed config object.
"""

from os.path import abspath, dirname, join
import yaml

def replace_template_vals(mycfg):
    """Replaces the template variables in config.yml"""
    return mycfg

cwd = dirname(__file__)
fpath = join(cwd, "config/config.yml")
with open(fpath, "r") as f:
    cfg = replace_template_vals(yaml.load(f))
