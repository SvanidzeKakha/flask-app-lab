from flask import Blueprint

post_bp = Blueprint("post", __name__, url_prefix="/post",
                    template_folder="templates",
                    static_folder="static",
                    static_url_path="static_for_post")

from . import views