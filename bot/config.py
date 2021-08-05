import yaml

secrets = yaml.load(open('.secrets.yaml'), Loader=yaml.Loader)

db_host = secrets["db_host"]
db_name = secrets["db_name"]

telegram_token = secrets["telegram_token"]

yandex = secrets["yandex"]
ya_password = secrets["ya_password"]
google = secrets["google"]
