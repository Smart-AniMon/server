from flask import Blueprint

from .views import (index, monitored, identified, 
                    not_identified, notification, 
                    history, flag)

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
bp.add_url_rule(
    "/notification", view_func=notification, endpoint="notification"
)
bp.add_url_rule(
    "/flag", view_func=flag, endpoint="flag", methods=['GET','POST']
)
bp.add_url_rule(
    "/history", view_func=history, endpoint="history",
)


def init_app(app):
    app.register_blueprint(bp)