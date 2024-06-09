import json
import os
from logging import getLogger, config, basicConfig, DEBUG, FileHandler

with open('./log/log_config.json', 'r') as f:
    print("a")
    log_conf = json.load(f)
print(log_conf)
config.dictConfig(log_conf)

# ここからはいつもどおり
#basicConfig(level=DEBUG)
if os.environ.get("environment") == "development":
    logger = getLogger("postgresql-api_info")
elif os.environ.get("environment") == "production":
    logger = getLogger("prod_loggers")
else:
    raise Exception("適切なロガーが設定されていません。")


logger.info("dkjdlkj")

# fh = FileHandler('/logs/info_logs.log')
# logger.addHandler(fh)
