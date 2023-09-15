import yaml
import os
from string import Template


def walk_dict_and_replace(d, **kwargs):
    for key, value in d.items():
        if isinstance(value, str):
            s = Template(value)
            d[key] = s.substitute(kwargs)
        if isinstance(value, dict):
            walk_dict_and_replace(value, **kwargs)


def load_and_replace(path: str) -> dict:
    with open(path, "r") as stream:
        conf = yaml.safe_load(stream)
        homedir = os.environ['HOME']
        walk_dict_and_replace(conf, home=homedir)
    return conf
