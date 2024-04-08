import configparser
import os

def load_config(filename=os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.ini")):
    config = configparser.ConfigParser()
    config.read(filename)
    return config

def get_section_config(section_name, config=load_config()):
    section_config = {}
    if section_name in config:
        section_config = dict(config[section_name])
    return section_config


config = get_section_config('BROWSER')
print(config['interval'])