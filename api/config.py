import yaml

DEFAULT_SECRET_PATH = "/etc/joker_api/secrets.yaml"
secrets = yaml.load(open(DEFAULT_SECRET_PATH), Loader=yaml.Loader)

db_host = secrets["db_host"]
db_name = secrets["db_name"]
