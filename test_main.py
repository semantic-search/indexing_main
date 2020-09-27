from task import main
from Services.YamlParserService import parse
import os

with open(yaml_file) as f:
    config_dict = yaml.safe_load(f)
main.delay("12.png", config_dict)