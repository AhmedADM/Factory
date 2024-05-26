

from factory_config import api, app

from factory_api import Home
from endpoints.item import MultipleItems, SingleItem
from endpoints.product import NewProduct, SingleProudct
from endpoints.size import MultipleSizes, SingleSize

api.add_resource(Home, "/home", strict_slashes=False)
api.add_resource(NewProduct, "/product", strict_slashes=False)
api.add_resource(SingleProudct, "/product/<int:product_id>" ,  strict_slashes=False)

api.add_resource(SingleSize, "/size/<int:size_id>", strict_slashes=False)
api.add_resource(MultipleSizes, "/product/<int:product_id>/sizes", strict_slashes=False)

api.add_resource(SingleItem, "/items/<int:item_id>", strict_slashes=False)
api.add_resource(MultipleItems, "/items", strict_slashes=False)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=6000)