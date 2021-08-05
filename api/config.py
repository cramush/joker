import yaml

secrets = yaml.load(open('.secrets.yaml'), Loader=yaml.Loader)

db_host = secrets["db_host"]
db_name = secrets["db_name"]
