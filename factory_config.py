
from configparser import ConfigParser
from flask import Blueprint, Flask, url_for
from flask_restx import Api

from endpoints.Item import MultipleItems, SingleItem
from factory_api import Home
from factory_db import FactoryDB
from endpoints.product import Product
from endpoints.size import MultipleSizes, SingleSize


app = Flask(__name__)
factory_home_bp = Blueprint("home", __name__, url_prefix="/home")


parser = ConfigParser()
parser.read("./app.conf")
db_configs = parser["Database"]

config = {}
config["DB_NAME"] = db_configs.get("db", "")
config["DB_PORT"] = int(db_configs.get("db_port", 0))
config["DB_USERNAME"] = db_configs.get("username", "")
config["DB_PASSWORD"] = db_configs.get("password", "")

print(config)


connection_str = f"postgresql+psycopg2://{config['DB_USERNAME']}:{config['DB_PASSWORD']}@127.0.0.1:{config['DB_PORT']}/{config['DB_NAME']}"

factory_db = FactoryDB(connection_str)
app.db = factory_db




class MyApi(Api):
    @property
    def specs_url(self):
        return url_for(self.endpoint('specs'), _external=True, _shceme='https')




# CORS(app, resources={r'/*': {'origins': '*'}})

api = MyApi(
    app,
    title="Factory Flask API",
    version="1.0",
    description="This is Factory API",
    doc="/docs"
)


api.add_resource(Home, "/home", strict_slashes=False)
api.add_resource(Product, "/product" ,"/product/<int:product_id>", strict_slashes=False)

api.add_resource(SingleSize, "/size/<int:size_id>", strict_slashes=False)
api.add_resource(MultipleSizes, "/product/<int:product_id>/sizes", strict_slashes=False)

api.add_resource(SingleItem, "/items/<int:item_id>", strict_slashes=False)
api.add_resource(MultipleItems, "/items", strict_slashes=False)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=6000)


