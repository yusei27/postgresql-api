import json
from logging import getLogger, config, basicConfig, DEBUG, FileHandler

with open('./log/log_config.json', 'r') as f:
    print("a")
    log_conf = json.load(f)
print(log_conf)
config.dictConfig(log_conf)

# ここからはいつもどおり
basicConfig(level=DEBUG)
logger = getLogger("postgresql-api_info")
logger.info("dkjdlkj")

# fh = FileHandler('/logs/info_logs.log')
# logger.addHandler(fh)
