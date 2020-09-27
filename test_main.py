from task import main
from Services.YamlParserService import parse
import os
parse(os.path.abspath("config.yaml"))
main.delay("12.png")