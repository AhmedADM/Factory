


swagger_product_add_data = {
            "data":{
                "description": "Product details",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "example": "butter"
                        },
                        "description": {
                            "type": "string",
                            "example": "butter ..."
                        },
                        "source": {
                            "type": "string",
                            "example": "Unkown"
                        },
                        "country": {
                            "type": "string",
                            "example": "Iraq"
                        },
                    }
                }

            }
        }


swagger_product_update_data = {
            "product_id": {
                    "description": "The Product id",
                    "in": "path",
                    "required": True
            },
            "data":{
                "description": "Product details",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string"
                        },
                        "description": {
                            "type": "string"
                        },
                        "source": {
                            "type": "string"
                        },
                        "country": {
                            "type": "string"
                        },
                    }
                }

            }
        }


product_id_param = {
                "product_id": {
                    "description": "The Product id",
                    "in": "path",
                    "required": True
                }
            }



size_id_param = {
            "size_id": {
                "description": "The Size id",
                "in": "path",
                "required": True
            }
        }


size_update_params = {
            "size_id": {
                "description": "The Size id",
                "in": "path",
                "required": True
            },
            "data":{
                "description": "Size details",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "sku": {
                            "type": "string"
                        },
                        "description": {
                            "type": "string"
                        },
                        "price": {
                            "type": "integer"
                        },
                        "size": {
                            "type": "string"
                        },
                    }
                }

            }
}



swagger_product_add_sizes_data = {
            "product_id": {
                    "description": "The Product id",
                    "in": "path",
                    "required": True
            },
            "data":{
                "description": "Sizes details",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "sku": {
                                "type": "string"
                            },
                            "description": {
                                "type": "string"
                            },
                            "price": {
                                "type": "integer"
                            },
                            "size": {
                                "type": "string"
                            },
                        }

                    }

                }

            }
        }


item_id_param = {
            "item_id": "The Item ID"
        }



swagger_item_update_data = {
            "item_id": {
                "description": "The Item ID",
                "in": "path",
                "required": True
            },
            "data":{
                "description": "Item details",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "issue_date": {
                            "type": "string",
                            "example": "1/1/2025"
                        },
                        "expire_date": {
                            "type": "string",
                            "example": "1/1/2027"
                        },
                        "status": {
                            "type": "string",
                            "enum": [ "Available", "Sold"],
                            "example": "Available"
                        }
                    }
                }

            }
}



swagger_add_items_data = {
            "data":{
                "description": "Items details",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "size_id": {
                                "type": "integer"
                            },
                            "issue_date": {
                                "type": "string",
                                "example": "1/1/2025"
                            },
                            "expire_date": {
                                "type": "string",
                                "example": "1/1/2027"
                            },
                            "status": {
                                "type": "string",
                                "enum": [ "Available", "Sold"],
                                "example": "Available"
                            }
                        }

                    }

                }

            }
        }
