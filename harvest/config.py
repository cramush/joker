import yaml

DEFAULT_SECRET_PATH = "/etc/harvest/secrets.yaml"
secrets = yaml.load(open(DEFAULT_SECRET_PATH), Loader=yaml.Loader)

db_login = secrets["db_login"]
db_password = secrets["db_password"]
db_host = secrets["db_host"]
db_name = secrets["db_name"]

password = secrets["password"]
login = secrets["login"]
recipient = secrets["recipient"]
