import json
from logging import getLogger, config, basicConfig, DEBUG

with open('./log/log_config.json', 'r') as f:
    print("a")
    log_conf = json.load(f)

config.dictConfig(log_conf)

# ここからはいつもどおり
basicConfig(level=DEBUG)
logger = getLogger(__name__)
logger.info("dkjdlkj")
