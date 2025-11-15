import os
from urllib.parse import urlparse

# If running on Heroku use JAWSDB
if "JAWSDB_URL" in os.environ:
    url = urlparse(os.environ["JAWSDB_URL"])

    MYSQL_HOST = url.hostname
    MYSQL_USER = url.username
    MYSQL_PASSWORD = url.password
    MYSQL_DB = url.path[1:]  # remove leading slash
else:
    # Local development
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "12345"
    MYSQL_DB = "to-do2025"
