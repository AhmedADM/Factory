import json

from factory_auth import auth
from factory_db import Item
from flask import  current_app,  jsonify, request
from flask_restx import Resource



class UnableToFindItem(Exception):
    pass

class UnableToAddItem(Exception):
    pass

class UnableToUpdateItem(Exception):
    pass

class UnableToDeleteItem(Exception):
    pass


class SingleItem(Resource):
    def get(self, item_id):
        try:
            item = current_app.db.get_single_item(item_id)
            if not item:
                raise UnableToFindItem(f"Unable to find item with id {item_id}")

            return jsonify(result=item, return_cod=0)

        except UnableToFindItem as ex:
            msg = str(ex)
            resp = jsonify(message=msg, return_code=1)
            resp.status_code = 500

            return resp

    @auth.login_required
    def put(self, item_id):
        try:
            if not request.data:
                resp = jsonify(message="Item data needed", return_code = 1)
                resp.status_code = 400
                return resp

            data = json.loads(request.data)

            item = current_app.db.update_item(item_id, **data)
            if not item:
                raise UnableToUpdateItem(f"Unable to update item with id {item_id}")

            return jsonify(message=f"Item with id {item_id} is successfully updated!", return_code=0)

        except UnableToUpdateItem as ex:
            msg = str(ex)
            resp = jsonify(message=msg, return_code=1)
            resp.status_code = 500

            return resp

    @auth.login_required
    def delete(self, item_id):
        """
        Delete single item
        :param item_id:
        :return:
        """
        try:
            deleted_item_id = current_app.db.delete_item(item_id)
            if not deleted_item_id:
                raise UnableToDeleteItem(f"Unable to delete size with id {item_id}")

            return jsonify(message=f"Size with id {item_id} is successfully deleted")
        except UnableToDeleteItem as ex:
            msg = str(ex)
            resp = jsonify(message = msg, return_code = 1)
            resp.status_code = 500

            return resp



class MultipleItems(Resource):
    # All items
    def get(self):
        """
        Get all items
        :return:
        """
        try:
            items = current_app.db.get_all_items()
            if not items:
                raise UnableToFindItem("Unable to load all itesm")

            return jsonify(result = items, return_code = 0)

        except UnableToFindItem as ex:
            msg = str(ex)
            resp = jsonify(message=msg, return_code=1)
            resp.status_code = 500

            return resp

    @auth.login_required
    def post(self):
        """
        Add multiple items
        :return:
        """
        try:
            if not request.data:
                resp = jsonify(message="Item data needed", return_code=1)
                resp.status_code = 400
                return resp

            data = json.loads(request.data)
            new_items = []

            for item in data:
                new_item = Item(**item)
                new_items.append(new_item)

            item_count = current_app.db.add_items(new_items)

            if not item_count:
                raise UnableToAddItem("Failed to add new items")

            return jsonify(message=f"{item_count} items Added!!")
        except UnableToAddItem as ex:
            msg = str(ex)
            resp = jsonify(message=msg, return_code=1)
            resp.status_code = 500

            return resp