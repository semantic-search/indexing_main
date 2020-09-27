from test_task import main
from Services.YamlParserService import parse
import os
parse(os.path.abspath("config.yaml"))
main("12.png")