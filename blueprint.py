from flask import Blueprint, redirect, render_template, request, url_for
from authlib.integrations.flask_client import OAuth, FlaskOAuth2App

from CTFd.cache import clear_user_session
from CTFd.models import Users, db
from CTFd.utils import get_config, set_config
from CTFd.utils.config.visibility import registration_visible
from CTFd.utils.decorators import admins_only
from CTFd.utils.helpers import error_for
from CTFd.utils.logging import log
from CTFd.utils.security.auth import login_user
from CTFd.utils.uploads import delete_file

from .models import OAuthClient
from .utils.user import generate_username
from .utils.db import get_oauth_client
from .utils.form import get_request_form_data
from .forms.client import OAuthClientCreationForm, OAuthClientUpdateForm
from .forms.global_settings import OAuthGlobalSettingsForm
from .constants.config import (
    SsoRegistrationTypes,
    SSO_ALLOW_REGISTRATION_KEY,
    SSO_VERIFY_USERS_KEY,
    DEFAULT_SSO_ALLOW_REGISTRATION,
    DEFAULT_SSO_VERIFY_USERS,
)

plugin_bp = Blueprint(
    "sso",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static/sso",
)


def load_bp(oauth: OAuth):
    ###########################################
    # Admin Views
    ###########################################

    @plugin_bp.route("/admin/sso", methods=["GET", "POST"])
    @admins_only
    def sso_list():
        if request.method == "POST":
            allow_registration = request.form["allow_registration"]
            verify_users = request.form.get("verify_users", False) in [
                True,
                "true",
                "True",
                "1",
                "y",
                "Y",
            ]

            set_config(SSO_ALLOW_REGISTRATION_KEY, allow_registration)
            set_config(SSO_VERIFY_USERS_KEY, verify_users)

        allow_registration = get_config(
            SSO_ALLOW_REGISTRATION_KEY, default=DEFAULT_SSO_ALLOW_REGISTRATION
        )
        verify_users = get_config(
            SSO_VERIFY_USERS_KEY, default=DEFAULT_SSO_VERIFY_USERS
        )

        return render_template(
            "sso_settings.html",
            form=OAuthGlobalSettingsForm(
                allow_registration=allow_registration,
                verify_users=verify_users,
            ),
        )

    @plugin_bp.route("/admin/sso/client/delete", methods=["POST"])
    @admins_only
    def sso_delete_client():
        data = request.form or request.get_json()
        ids = data.get("client_ids", "").split(",")

        for client in OAuthClient.query.filter(OAuthClient.id.in_(ids)).all():
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

    @plugin_bp.route(
        "/admin/sso/client/update/<string:client_id>", methods=["GET", "POST"]
    )
    @admins_only
    def sso_details(client_id):
        client = get_oauth_client(client_id)
        if not client:
            return redirect(url_for("sso.sso_list"))

        if request.method == "POST":
            request_data = get_request_form_data()
            for key, value in request_data.items():
                setattr(client, key, value)
            db.session.commit()
            db.session.flush()

            client.update(oauth)

            return redirect(url_for("sso.sso_list"))

        else:
            form = OAuthClientUpdateForm(**client.__dict__)
            return render_template("details.html", form=form)

    @plugin_bp.route("/admin/sso/client/create", methods=["GET", "POST"])
    @admins_only
    def sso_create():
        if request.method == "POST":
            request_data = get_request_form_data()
            client = OAuthClient(**request_data)
            db.session.add(client)
            db.session.commit()
            db.session.flush()

            client.register(oauth)

            return redirect(url_for("sso.sso_list"))

        else:
            form = OAuthClientCreationForm()
            return render_template("create.html", form=form)

    ###########################################
    # Auth Views
    ###########################################

    @plugin_bp.route("/sso/login/<string:client_id>", methods=["GET"])
    def sso_oauth(client_id):
        client: FlaskOAuth2App = oauth.create_client(client_id)
        redirect_uri = url_for("sso.sso_redirect", client_id=client_id, _external=True)
        return client.authorize_redirect(redirect_uri)

    @plugin_bp.route("/sso/redirect/<string:client_id>", methods=["GET"])
    def sso_redirect(client_id):
        client: FlaskOAuth2App = oauth.create_client(client_id)
        db_client = get_oauth_client(client_id)

        token = client.authorize_access_token()
        user_info = client.userinfo()

        user_email = user_info[db_client.email_claim]
        user_roles = user_info.get("roles")  # TODO: manage this

        user = Users.query.filter_by(email=user_email).first()
        if user is None:
            # Check if we are allowing registration before creating users
            sso_registration_alowed = get_config(
                SSO_ALLOW_REGISTRATION_KEY,
                default=DEFAULT_SSO_ALLOW_REGISTRATION,
            )

            if sso_registration_alowed == SsoRegistrationTypes.ALWAYS or (
                sso_registration_alowed == SsoRegistrationTypes.WHEN_ENABLED
                and registration_visible()
            ):
                user = Users(
                    name=generate_username(user_info, db_client),
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

        if bool(get_config(SSO_VERIFY_USERS_KEY, default=DEFAULT_SSO_VERIFY_USERS)):
            user.verified = True

        db.session.commit()

        if (
            user_roles is not None
            and len(user_roles) > 0
            and user_roles[0] in ["admin", "user"]
        ):
            user_role = user_roles[0]
            if user_role != user.type:
                user.type = user_role
                db.session.commit()
                user = Users.query.filter_by(email=user_email).first()
                clear_user_session(user_id=user.id)

        login_user(user)

        return redirect(url_for("challenges.listing"))

    return plugin_bp
