import json
from flask import  current_app,  jsonify, request
from flask_restx import Resource

from factory_auth import auth
from factory_db import Size


class UnableToFindSize(Exception):
    pass

class UnableToAddSize(Exception):
    pass

class UnableToUpdateSize(Exception):
    pass

class UnableToDeleteSize(Exception):
    pass



class SingleSize(Resource):
    def get(self, size_id):
        """
        Get Size details
        :param size_id:
        :return:
        """
        try:
            size = current_app.db.get_size(size_id)
            if not size:
                raise UnableToFindSize(f"Size with id {size_id} does not exist.")

            return jsonify(result = size, return_code = 0)
        except UnableToFindSize as ex:
            msg = str(ex)
            resp = jsonify(message = msg, return_code = 1)
            resp.status_code = 500

            return resp

    @auth.login_required
    def put(self, size_id):
        """
        Update size details
        :param size_id:
        :return:
        """
        try:
            if not request.data:
                resp = jsonify(message="Size data needed", return_code = 1)
                resp.status_code = 400
                return resp

            data = json.loads(request.data)

            size = current_app.db.update_size(size_id, **data)
            if not size:
                raise UnableToUpdateSize(f"Unable to update size with id {size_id}")

            return jsonify(message=f"Size with id {size_id} is successfully updated!", return_code=0)

        except UnableToUpdateSize as ex:
            msg = str(ex)
            resp = jsonify(message=msg, return_code=1)
            resp.status_code = 500

            return resp

    @auth.login_required
    def delete(self, size_id):
        """
        Delete single size
        :param size_id:
        :return:
        """
        try:
            deleted_size_id = current_app.db.delete_size(size_id)
            if not deleted_size_id:
                raise UnableToDeleteSize(f"Unable to delete size with id {size_id}")

            return jsonify(message=f"Size with id {size_id} is successfully deleted")
        except UnableToDeleteSize as ex:
            msg = str(ex)
            resp = jsonify(message = msg, return_code = 1)
            resp.status_code = 500

            return resp


class MultipleSizes(Resource):
    def get(self, product_id):
        """
        Get sizes of product ID
        :param product_id:
        :return:
        """
        try:
            sizes = current_app.db.get_product_sizes(product_id)
            if not sizes:
                raise UnableToFindSize(f"Sizes with product id {product_id} does not exists.")
            return jsonify(result=sizes, return_code = 0)
        except UnableToFindSize as ex:
            msg = str(ex)
            return {
                "message": msg,
                 "return_code" : 1
            }, 404

    @auth.login_required
    def put(self, product_id):
        """
        Add multiple sizes to a specific product ID
        :param product_id:
        :return:
        """
        try:

            if not request.data:
                resp = jsonify(message="Size data needed", return_code=1)
                resp.status_code = 400
                return resp


            data = json.loads(request.data)

            new_sizes = []

            for size in data:
                size['product_id'] = product_id
                new_size = Size(**size)
                new_sizes.append(new_size)

            size_count = current_app.db.add_sizes(new_sizes)

            if not size_count:
                raise UnableToAddSize("Failed to add new product sizes")

            return jsonify(message=f"{size_count} sizes with product id {product_id} is Added!!")
        except UnableToAddSize as ex:
            msg = str(ex)
            return {
                "message": msg,
                "return_code": 1
            }, 500
