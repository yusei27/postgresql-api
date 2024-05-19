#
# Gunicorn config file
#
wsgi_app = 'app:app'#:application'

# Server Mechanics
#========================================
# current directory
#chdir = '/work/python/gunic/gu'
#chdir = '../'

#hhtps ssl certificate
certfile = './network/server.crt'
keyfile = './network/server.key'

# daemon mode
daemon = False

# enviroment variables
# raw_env = [
#     'ENV_TYPE=dev',
#     'HOGEHOGE_KEY=xxxxxxxxxxxxxxxxxxxxxxxxx'
# ]

# Server Socket
#========================================
bind = '0.0.0.0:3334'

# Worker Processes
#========================================
workers = 2

#  Logging
#========================================
# access log
# accesslog = '/work/python/gunic/gu/logs/access.log'
accesslog = '/logs/postgresql-api_info.log'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# # gunicorn log
errorlog = '-'
loglevel = 'info'