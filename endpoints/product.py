import json
from flask import  current_app,  jsonify, request
from flask_restx import Resource

from factory_auth import auth
from factory_config import api
from factory_doc import product_id_param, swagger_product_update_data, swagger_product_add_data


class UnableToFindProduct(Exception):
    pass

class UnableToAddProduct(Exception):
    pass

class UnableToUpdateProduct(Exception):
    pass


class UnableToDeleteProduct(Exception):
    pass




class SingleProudct(Resource):
    @api.doc( params= product_id_param  )
    def get(self, product_id):
        """
        Get Product details
        :param product_id:
        :return:
        """
        try:
            product = current_app.db.get_product(product_id)
            if not product:
                raise UnableToFindProduct(f"Product with id {product_id} does not exists.")
            return jsonify(result=product, return_code=0)
        except UnableToFindProduct as ex:
            msg = str(ex)
            return {
                "message": msg,
                "return_code": 1
            }, 404

    @api.doc( params=swagger_product_update_data )
    @auth.login_required
    def put(self, product_id):
        """
        Update single product
        :param product_id:
        :return:
        """
        try:
            if not request.data:
                return {
                    "message": "Additional product data needed",
                    "return_code": 1
                }, 400

            data = json.loads(request.data)

            product = current_app.db.update_product(product_id, **data)
            if not product:
                raise UnableToUpdateProduct(f"Unable to update product with id {product_id}")

            return jsonify(message=f"Product with id {product_id} is successfully updated!", return_code=0)

        except UnableToUpdateProduct as ex:
            msg = str(ex)
            return {
                "message": msg,
                "return_code": 1
            }, 500

    @api.doc(params=product_id_param)
    @auth.login_required
    def delete(self, product_id):
        """
        Delete single product
        :param product_id:
        :return:
        """
        try:
            deleted_product_id = current_app.db.delete_product(product_id)
            if not deleted_product_id:
                raise UnableToDeleteProduct(f"Unable to delete product with id {product_id}")

            return jsonify(message=f"Product with id {product_id} is successfully deleted")

        except UnableToDeleteProduct as ex:
            msg = str(ex)
            return {
                "message": msg,
                "return_code": 1
            }, 500
        except Exception as ex:
            msg = str(ex)
            return {
                "message": msg,
                "return_code": 1
            }, 500


# Product CRUD
class NewProduct(Resource):

    @api.doc( params = (swagger_product_add_data) )
    @auth.login_required
    def post(self):
        """
        Add single product
        :return:
        """
        try:

            if not request.data:
                return {
                    "message": "Product data needed",
                    "return_code": 1
                }, 400

            data = json.loads(request.data)
            new_product = current_app.db.add_product(data)
            if not new_product:
                raise UnableToAddProduct("Failed to add new product")
            return jsonify(message=f"Product with id {new_product.get('id')} is Added!!")
        except UnableToAddProduct as ex:
            msg = str(ex)
            return {
                "message": msg,
                "return_code": 1
            }, 500

