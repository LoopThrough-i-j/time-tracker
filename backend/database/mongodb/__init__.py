from urllib.parse import quote_plus as parse_url

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from environment import EnvironmentVariables

mongo_uri = EnvironmentVariables.MONGO_URI_FORMAT.format(
    parse_url(EnvironmentVariables.MONGO_USERNAME),
    parse_url(EnvironmentVariables.MONGO_PASSWORD),
    EnvironmentVariables.MONGO_HOST,
    EnvironmentVariables.MONGO_PORT,
)

mongo_client = MongoClient(
    mongo_uri,
    server_api=ServerApi("1"),
    tz_aware=True,
)

mongo_db = mongo_client[EnvironmentVariables.MONGO_DATABASE]
