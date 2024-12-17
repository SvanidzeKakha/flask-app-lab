from flask import Blueprint

users_bp = Blueprint("users", __name__,
                    url_prefix="/users",
                    static_folder="static",
                    template_folder="templates/users")

from . import views