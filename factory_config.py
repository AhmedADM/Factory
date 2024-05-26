
from configparser import ConfigParser
from flask import Blueprint, Flask, url_for
from flask_cors import CORS
from flask_restx import Api


from factory_api import Home
from factory_db import FactoryDB



app = Flask(__name__)
factory_home_bp = Blueprint("home", __name__, url_prefix="/home")


parser = ConfigParser()
parser.read("./app.conf")
db_configs = parser["Database"]

config = {}
config["DB_NAME"] = db_configs.get("db", "")
config["DB_HOST"] = db_configs.get("db_host", "localhost")
config["DB_PORT"] = int(db_configs.get("db_port", 0))
config["DB_USERNAME"] = db_configs.get("username", "")
config["DB_PASSWORD"] = db_configs.get("password", "")

print(config)


connection_str = f"postgresql+psycopg2://{config['DB_USERNAME']}:{config['DB_PASSWORD']}@{config['DB_HOST']}:{config['DB_PORT']}/{config['DB_NAME']}"

factory_db = FactoryDB(connection_str)
app.db = factory_db


authorizarions = {
    "BasiceAuth": {
        "type": "basic"
    }
}


class MyApi(Api):
    @property
    def specs_url(self):
        return url_for(self.endpoint('specs'))




api = MyApi(
    app,
    title="Factory Flask API",
    version="1.0",
    description="This is Factory API",
    default="Factory",
    authorizations=authorizarions
)


CORS(app)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=6000)


