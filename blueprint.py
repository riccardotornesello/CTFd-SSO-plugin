from flask import Blueprint, redirect, render_template, request, url_for

from CTFd.cache import clear_user_session
from CTFd.models import Users, db
from CTFd.utils.config.visibility import registration_visible
from CTFd.utils.decorators import admins_only
from CTFd.utils.helpers import error_for
from CTFd.utils.logging import log
from CTFd.utils.security.auth import login_user
from CTFd.utils.uploads import upload_file, delete_file

from .models import OAuthClients
from .utils.user import generate_username
from .utils.db import update_oauth_config_key, get_all_oauth_config, get_oauth_config
from .forms.creation import OAuthClientCreationForm
from .forms.global_settings import OAuthGlobalSettingsForm
from .constants.config import SsoConfigTypes, SsoRegistrationTypes

plugin_bp = Blueprint(
    "sso", __name__, template_folder="templates", static_folder="static", static_url_path="/static/sso"
)


def load_bp(oauth):
    @plugin_bp.route("/admin/sso", methods=["GET", "POST"])
    @admins_only
    def sso_list():
        if request.method == "POST":
            allow_registration = request.form["allow_registration"]
            update_oauth_config_key(SsoConfigTypes.SSO_ALLOW_REGISTRATION, allow_registration)

        current_config = get_all_oauth_config()

        return render_template(
            "sso_settings.html",
            form=OAuthGlobalSettingsForm(allow_registration=current_config.get(SsoConfigTypes.SSO_ALLOW_REGISTRATION)),
        )

    @plugin_bp.route("/admin/sso/client/delete", methods=["POST"])
    @admins_only
    def sso_delete_client():
        data = request.form or request.get_json()
        ids = data.get("client_ids", "").split(",")

        for client in OAuthClients.query.filter(OAuthClients.id.in_(ids)).all():
            client.disconnect(oauth)
            if client.icon:
                try:
                    delete_file(client.icon)
                except:
                    pass
            db.session.delete(client)
            db.session.commit()
            db.session.flush()

        return "ok"

    @plugin_bp.route("/admin/sso/client/<int:client_id>", methods=["GET"])
    @admins_only
    def sso_details(client_id):
        client = OAuthClients.query.filter_by(id=client_id).first()
        if not client:
            return redirect(url_for("sso.sso_list"))

        form = OAuthClientCreationForm(**client.__dict__)
        return render_template("details.html", form=form, client=client)

    @plugin_bp.route("/admin/sso/create", methods=["GET", "POST"])
    @admins_only
    def sso_create():
        if request.method == "POST":
            name = request.form["name"]
            client_id = request.form["client_id"]
            client_secret = request.form["client_secret"]
            access_token_url = request.form["access_token_url"]
            authorize_url = request.form["authorize_url"]
            api_base_url = request.form["api_base_url"]
            scope = request.form["scope"]
            text_color = request.form.get("text_color")
            background_color = request.form.get("background_color")
            icon = request.files.get("icon")

            if icon:
                f = upload_file(file=icon)
                icon = f.id
            else:
                icon = None

            client = OAuthClients(
                name=name,
                client_id=client_id,
                client_secret=client_secret,
                access_token_url=access_token_url,
                authorize_url=authorize_url,
                api_base_url=api_base_url,
                scope=scope,
                text_color=text_color,
                background_color=background_color,
                icon=icon,
            )
            db.session.add(client)
            db.session.commit()
            db.session.flush()

            client.register(oauth)

            return redirect(url_for("sso.sso_list"))

        form = OAuthClientCreationForm()
        return render_template("create.html", form=form)

    @plugin_bp.route("/sso/login/<int:client_id>", methods=["GET"])
    def sso_oauth(client_id):
        client = oauth.create_client(client_id)
        redirect_uri = url_for("sso.sso_redirect", client_id=client_id, _external=True)
        return client.authorize_redirect(redirect_uri)

    @plugin_bp.route("/sso/redirect/<int:client_id>", methods=["GET"])
    def sso_redirect(client_id):
        client = oauth.create_client(client_id)
        client.authorize_access_token()
        api_data = client.get("").json()

        user_name = generate_username(api_data)
        user_email = api_data["email"]
        user_roles = api_data.get("roles")

        user = Users.query.filter_by(email=user_email).first()
        if user is None:
            # Check if we are allowing registration before creating users
            sso_registration_alowed = get_oauth_config(SsoConfigTypes.SSO_ALLOW_REGISTRATION)

            if sso_registration_alowed == SsoRegistrationTypes.ALWAYS or (
                sso_registration_alowed == SsoRegistrationTypes.WHEN_ENABLED and registration_visible()
            ):
                user = Users(
                    name=user_name,
                    email=user_email,
                    verified=True,
                )
                db.session.add(user)
                db.session.commit()
            else:
                log("logins", "[{date}] {ip} - Public registration via MLC blocked")
                error_for(
                    endpoint="auth.login",
                    message="Public registration is disabled. Please try again later.",
                )
                return redirect(url_for("auth.login"))

        user.verified = True
        db.session.commit()

        if user_roles is not None and len(user_roles) > 0 and user_roles[0] in ["admin", "user"]:
            user_role = user_roles[0]
            if user_role != user.type:
                user.type = user_role
                db.session.commit()
                user = Users.query.filter_by(email=user_email).first()
                clear_user_session(user_id=user.id)

        login_user(user)

        return redirect(url_for("challenges.listing"))

    return plugin_bp
