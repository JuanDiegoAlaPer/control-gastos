from flask import Blueprint
providers = Blueprint("providers",
                     __name__,
                     url_prefix="/api/v1/providers")

@providers.get("/<int:id>/products")
def read_providers(id):
    return "Reading products from a provider ... soon"