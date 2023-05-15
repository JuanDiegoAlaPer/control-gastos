from flask import Blueprint, request
products = Blueprint("products",
                     __name__,
                     url_prefix="/api/v1/products")

# Data for example purposes
product_data = [
 {"id": 1, "name": "Papitas", "price": 1000, "expiration": "2020-01-12"},
 {"id": 2, "name": "Gomitas", "price": 2000, "expiration": "2020-02-22"},
 {"id": 3, "name": "Frunas", "price": 3000, "expiration": "2022-03-11"},
 {"id": 4, "name": "Juguito", "price": 4000, "expiration": "2022-03-18"},
 {"id": 5, "name": "Galletas", "price": 5000, "expiration": "2025-04-15"},
];



@products.get("/")
def read_all():
    return {"data": product_data}, 200


@products.get("/<int:id>")
def read_one(id):
    for product in product_data:
        if product['id'] == id:
            return {"data": product}, 200

    return {"error": "Resource not found"}, 404


# @products.post("/")
# def create():
#     return "Creating a product ... soon"

@products.post("/")
def create():
    post_data = request.get_json()

    product = {
        "id": len(product_data) + 1,
        "name": post_data.get('name', 'No Name'),
        "price": post_data.get('price', 0),
        "expiration": post_data.get('expiration', None)
    }

    product_data.append(product)

    return {"data": product}, 201


# @products.put('/<int:id>')
# @products.patch('/<int:id>')
# def update(id):
#     return "Updating a product ... soon"

@products.put('/<int:id>')
@products.patch('/<int:id>')
def update(id):
    post_data = request.get_json()
    for i in range(len(product_data)):
        if product_data[i]['id'] == id:
            product_data[i] = {
                            "id": id,
                            "name": post_data.get('name'),
                            "price": post_data.get('price'),
                            "expiration": post_data.get('expiration')
                        }
            return {"data": product_data[i]}, 200
    return {"error": "Resource not found"}, 404


# @products.delete("/<int:id>")
# def delete(id):
#     return "Removing a product ... soon"

@products.delete("/<int:id>")
def delete(id):
    for i in range(len(product_data)):
        if product_data[i]['id'] == id:
            del product_data[i]
            return {"data": ""}, 204
    return {"error": "Resource not found"}, 404

@products.get("/<int:id>/providers")
def read_providers(id):
    return "Reading providers from a product ... soon"
