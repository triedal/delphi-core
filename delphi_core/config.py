from os.path import abspath, dirname, join
import yaml

def replace_template_vals(cfg):
    cfg['paths']['proj_root'] = dirname(dirname(abspath(__file__)))
    return cfg

cwd = dirname(__file__)
fpath = join(cwd, "config/config.yml")
with open(fpath, "r") as f:
    cfg = replace_template_vals(yaml.load(f))