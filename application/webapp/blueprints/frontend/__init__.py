from flask import Blueprint

from .views import index, monitored, identified, not_identified

bp = Blueprint("frontend", __name__, template_folder="template")

bp.add_url_rule("/", view_func=index)
bp.add_url_rule(
    "/monitored", view_func=monitored, endpoint="monitored"
)
bp.add_url_rule(
    "/identified", view_func=identified, endpoint="identified"
)
bp.add_url_rule(
    "/not-identified", view_func=not_identified, endpoint="not_identified"
)


def init_app(app):
    app.register_blueprint(bp)