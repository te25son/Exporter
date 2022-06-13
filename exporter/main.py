from flask import Blueprint, render_template, request, session
from .library.helpers import main_action, login_required, no_direct_url_access
from .library.context import Context
from .forms.main_forms import ExportForm
from .components.user_component import UserComponent
from .components.export_component import ExportComponent


Users = UserComponent()
Exporter = ExportComponent()
main = Blueprint("main", __name__, template_folder="templates")


@main.route("/", methods=["GET"])
@login_required
@main_action
def home(context: Context) -> str:
    """
    View for returning the home page.

    Cannot be accessed unless a user is already logged in.
    """
    return render_template(context.template, is_user=True)


@main.route("/export", methods=["GET", "POST"])
@login_required
@no_direct_url_access
@main_action
def export(context: Context):
    """
    View for displaying the export page. The page is not
    directly accessible, so any attempt by a user to navigate
    to `https//www.this-website/export` would redirect them
    back to the home page.

    The average user is also directed to an invalid page if
    they do not have the right credentials.

    A user with the right credentials or with the ability
    to export, is shown the form and can make a POST action.
    """
    form = ExportForm(request.form)
    user = Users.get_by_username(session["username"])

    if not user or not user.can_export:
        return render_template("main/invalid.html")

    if request.method == "POST" and form.validate():
        return {
            "success": Exporter.try_export(form.queue_id.data, form.annotation_id.data)
        }

    return render_template(context.template, form=form)
